import unittest
from kite_connection_manager.connection_manager import KiteConnectionManager


class MyTestCase(unittest.TestCase):
    def test_something(self):
        # creds = {
        #     "name": "Aneesha Kaushal",
        #     "user_name": "JFA773",
        #     "password": "buy@Farm1",
        #     "api_key": "97wr0exmsqicnu01",
        #     "api_secret": "ntos88g38uma3jkyczhg7ac6g8ar4pj5",
        #     "google_authenticator_secret": "7JCJA4VDGVCWUGDPRKVK3RGYVOB3F3EF",
        #     "quantity_multiplier": 0.5
        # }
        creds = {'name': 'Shashwat Rastogi HUF', 'user_name': 'CWQ945', 'password': 'make@Money2',
                 'api_key': 'j5jtfv7n4yt1y8vt', 'api_secret': 'q0q1v2tfdt25r4pzvgppafxdhb9d2y98',
                 'google_authenticator_secret': 'BDPFWPFEFEKJEWDAE7GPUSLSLP4RJ4JS', 'quantity_multiplier': 0.4}
        connection_manager = KiteConnectionManager(user_details=creds, refresh_connection=False)
        connection_manager.get_kite_connect()
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
