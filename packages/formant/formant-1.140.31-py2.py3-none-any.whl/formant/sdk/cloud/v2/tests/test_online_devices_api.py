import unittest
from formant.sdk.cloud.v2.src.query_api import QueryAPI

import dateutil.parser as parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestOnlineDevices(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestOnlineDevices, self).__init__(*args, **kwargs)
        self.client = QueryAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_online(self):
        response = self.client.online_devices.online()
        self.assertEqual(response.status_code, 200)


unittest.main()
