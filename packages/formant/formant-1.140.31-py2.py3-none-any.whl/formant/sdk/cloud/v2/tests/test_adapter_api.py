import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.src.resources.adapters import *
import os
import json

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestAdapters(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAdapters, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    # def test_create_adapter(self):
    #     name = "generic-test"
    #     file_id = "cd860575-df44-40ea-a1ef-c5860c1a8992"
    #     exec_command = "test"
    #     adapter = Adapter(name, file_id, exec_command)
    #     result = self.client.adapters.create(adapter)
    #     self.assertEqual(result.status_code, 201)
    #     content = json.loads(result.content)
    #     id = content["id"]
    #     result = self.client.adapters.delete(id)
    #     self.assertEqual(result.status_code, 204)


unittest.main()
