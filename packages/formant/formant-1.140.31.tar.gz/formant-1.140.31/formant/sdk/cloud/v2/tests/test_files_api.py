import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
import os
import aiounittest
import uuid

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestFiles(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestFiles, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_upload(self):
        random_name = str(uuid.uuid4())
        file = open(f"{random_name}.txt", "w")
        file.write("Sample Data")
        file.close()
        path = file.name
        result = self.client.files.upload(path)
        os.remove(path)
        self.assertTrue(result)


class TestFilesAsync(aiounittest.AsyncTestCase):
    def __init__(self, *args, **kwargs):
        super(TestFilesAsync, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    async def test_async_upload(self):
        random_name = str(uuid.uuid4())
        file = open(f"test_{random_name}.txt", "w")
        file.write("Sample Data")
        file.close()
        path = file.name
        result = await self.client.files.upload_async(path)
        os.remove(path)
        self.assertTrue(result)


unittest.main()
