from .connect_without_apikey import KiteConnectBrowser
from .utils import get_totp
from .repeat_timer import RepeatTimer
import logging
import pickle
from datetime import datetime
import os
from typing import Optional
from kiteconnect import KiteConnect
from kiteconnect.exceptions import KiteException
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse
from urllib.parse import parse_qs
from smart_open import open

logger = logging.getLogger(__name__)


class ZerodhaLoginException(Exception):
    """
    Exception raised while logging into Zerodha.
    """

    def __init__(self, config, error=None, message="Failed to login to Zerodha!"):
        super().__init__("{}\nProvided config: {}\n{}".format(message, config, "Error from client: {}".format(
            error) if error is not None else ""))


class KiteConnectionManager:
    """
    This class is responsible to login to Zerodha and return the KiteConnect handle through which we can act upon
    the particular account.

    @:param user_details dictionary containing login credentials - user_name, password, pin, google_authenticator_secret
        ,api_key, api_secret
    @:param refresh_connection: if true refresh the connection every refresh_interval_minutes
    @:param session_dir: directory where sessions would be saved to prevent re-login during restarts
    """
    __DATE_TODAY = datetime.now().strftime('%Y_%m_%d')
    __CHROME_DRIVER_FILE_PATH = '/usr/local/bin/chromedriver'

    def __init__(self, user_details: dict, refresh_connection: bool = False, refresh_interval_minutes: int = 10,
                 session_base_dir: str = os.getcwd()):
        if 'user_name' not in user_details or 'password' not in user_details:
            raise ZerodhaLoginException(config=user_details, message="Must have both user_name and password set")
        if 'pin' not in user_details and 'google_authenticator_secret' not in user_details:
            raise ZerodhaLoginException(config=user_details,
                                        message="One of pin or google_authenticator_secret must be provided!")
        self.config = user_details
        self.user_name = user_details.get('user_name', None)
        self.password = user_details.get('password', None)
        self.api_key = user_details.get('api_key', None)
        self.api_secret = user_details.get('api_secret', None)
        self.pin = user_details.get('pin', None)
        self.google_authenticator_secret = user_details.get('google_authenticator_secret', None)
        self.kite: KiteConnect = None
        self.use_api_key = self.api_key is not None and self.api_secret is not None
        self.session_dir = '{dir}/{date}'.format(dir=session_base_dir, date=KiteConnectionManager.__DATE_TODAY)
        if refresh_connection:
            self.background_thread = RepeatTimer(refresh_interval_minutes * 60, self.get_kite_connect)

    def __get_session_file_path(self):
        return '{dir}/{user}_{login_type}.session'.format(dir=self.session_dir,
                                                          user=self.user_name,
                                                          login_type='api' if self.is_using_api_key() else 'browser')

    def is_using_api_key(self) -> bool:
        return self.use_api_key

    def is_logged_in(self) -> bool:
        """
        Since, KiteConnect doesn't provide a clean way to check if the access token is valid. We will try to fetch the
        price of an instrument and see if a valid response is return. If we see a status code of 403 , it means that
        the session is expired. Check https://kite.trade/docs/connect/v3/exceptions/#common-http-error-codes to learn
        about error codes.

        @:return True if the KiteConnect is still valid
        """
        if not self.kite:
            if not self.__load_session():
                return False
        # If using API KEY, the access token stays valid for a day so no need to check for login
        if self.is_using_api_key():
            return True
        try:
            self.kite.ltp("NSE:INFY")
        except KiteException as ke:
            if ke.code == 403:
                return False
            raise ke
        return True

    def shutdown(self, invalidate_access_token=False):
        if self.background_thread:
            self.background_thread.cancel()
        # TODO: Need to be adapted for GCS
        # if invalidate_access_token and self.is_using_api_key():
        #     logger.info('Invalidating access_token for the user %s', self.user_name)
        #     self.kite.invalidate_access_token()
        #     logger.info('Clearing up session file for user %s at %s', self.user_name, self.__get_session_file_path())
        #     os.remove(self.__get_session_file_path())

    def __dump_session(self):
        with open(self.__get_session_file_path(), 'wb') as handle:
            pickle.dump(self.kite, handle, protocol=pickle.HIGHEST_PROTOCOL)
            logger.info('Dumped KiteConnect object for user %s at %s', self.user_name, self.__get_session_file_path())

    def __load_session(self) -> bool:
        file_path = self.__get_session_file_path()
        try:
            with open(file_path, 'rb') as handle:
                loaded_session = pickle.load(handle)
                # if self.is_using_api_key():
                #     self.kite.renew_access_token(refresh_token=self.kite.access_token, api_secret=self.api_secret)
                #     self.__dump_session()
                if not isinstance(loaded_session, KiteConnect):
                    return False
                self.kite = loaded_session
                return True
        except Exception as ioe:
            logger.info('Unable to load KiteConnect object for user %s from %s. Error: %s', self.user_name,
                        file_path, ioe)
            return False

    def get_kite_connect(self) -> KiteConnect:
        if not self.is_logged_in():
            self.kite = self.__login()
            self.__dump_session()
        return self.kite

    def __login(self) -> KiteConnect:
        """
        Login a user and fetch the corresponding KiteConnect handle
        """
        logger.info('Trying to login user_id %s', self.user_name)
        if self.is_using_api_key():
            return self.__login_with_apikey()
        return self.__login_without_apikey()

    def __login_without_apikey(self) -> KiteConnect:
        kite_connect_browser = KiteConnectBrowser(user_id=self.user_name, password=self.password,
                                                  google_authenticator_secret=self.google_authenticator_secret,
                                                  pin=self.pin)
        try:
            kite_connect_browser.login()
        except Exception as e:
            raise ZerodhaLoginException(self.config, e)
        logger.info("Successfully logged in %s without API Key", self.user_name)
        return kite_connect_browser

    def __login_with_apikey(self, retry_attempt=1) -> KiteConnect:
        """
        Establishes connection to Kite by "always" generating a new session.
        """
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument("--window-size=1920,1080")
        driver = webdriver.Chrome(self.__CHROME_DRIVER_FILE_PATH, options=chrome_options)
        driver.implicitly_wait(5)
        try:
            import time
            kite = KiteConnect(api_key=self.api_key)
            driver.get(kite.login_url())

            WebDriverWait(driver=driver, timeout=10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='login-form']")))
            driver.find_element(By.XPATH, "//input[@type='text']").send_keys(self.user_name)
            driver.find_element(By.XPATH, "//input[@type='password']").send_keys(self.password)
            time.sleep(0.5)
            driver.find_element(By.XPATH, "//button[@type='submit']").click()

            time.sleep(0.5)
            WebDriverWait(driver=driver, timeout=10).until(
                EC.visibility_of_element_located((By.XPATH, "//div[@class='login-form']")))
            driver.find_element(By.XPATH, "//input[@type='text']").send_keys(
                get_totp(self.google_authenticator_secret) if self.pin is None else self.pin)

            time.sleep(0.5)
            request_token = KiteConnectionManager.__extract_request_token(driver.current_url)
            kite.generate_session(request_token, api_secret=self.api_secret)
            logger.info("Successfully logged in %s using API Key %s. Request Token: %s", self.user_name, self.api_key,
                        request_token)
            return kite
        except Exception as e:
            if retry_attempt > 3:
                raise ZerodhaLoginException(self.config, e)
            time.sleep(1)
            self.__login_with_apikey(retry_attempt=retry_attempt+1)
        finally:
            driver.close()
            driver.quit()

    @staticmethod
    def __extract_request_token(redirect_url: str) -> str:
        """
        Extracts request_token from the redirect_url
        :param redirect_url: The URL to which Kite API redirects to after successful login
        """
        try:
            parsed_url = urlparse(redirect_url)
            return parse_qs(parsed_url.query)['request_token'][0]
        except Exception as e:
            logger.error('Unable to extract request token from the redirect URL %s', redirect_url)
