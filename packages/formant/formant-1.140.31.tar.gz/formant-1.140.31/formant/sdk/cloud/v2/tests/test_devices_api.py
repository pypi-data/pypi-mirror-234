import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import (
    DeviceQuery,
    PartialDevice,
    DeviceConfiguration,
    DeviceConfigurationDocument,
)
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestDevices(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestDevices, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_query_without_params(self):
        device_query = DeviceQuery()
        result = self.client.devices.query(device_query)
        self.assertEqual(result.status_code, 200)

    def test_query_with_params(self):
        json_params = {"name": "model00.001", "tags": {"location": ["sf", "la"]}}
        device_query = DeviceQuery(**json_params)
        result = self.client.devices.query(device_query)
        self.assertEqual(result.status_code, 200)

    def test_patch(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        json_params = {"enabled": True}
        partial_device = PartialDevice(**json_params)
        result = self.client.devices.patch(device_id, partial_device)
        self.assertEqual(result.status_code, 200)

    def test_get_device(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        result = self.client.devices.get_device(device_id)
        self.assertEqual(result.status_code, 200)

    def test_get_device_configuration(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        desired_configuration_version = 3
        result = self.client.devices.get_device_configuration(
            device_id, desired_configuration_version
        )
        self.assertEqual(result.status_code, 200)

    def test_post_device_configuration(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        device_configuration_document = DeviceConfigurationDocument()
        device_configuration = DeviceConfiguration(device_configuration_document)
        result = self.client.devices.post_device_configuration(
            device_id, device_configuration
        )
        self.assertEqual(result.status_code, 201)


unittest.main()
