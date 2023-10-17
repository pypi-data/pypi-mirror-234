import unittest
from formant.sdk.cloud.v2.src.query_api import QueryAPI
from formant.sdk.cloud.v2.formant_query_api_client.models.scope_filter import (
    ScopeFilter,
)
import dateutil.parser as parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestMetadata(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestMetadata, self).__init__(*args, **kwargs)
        self.client = QueryAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_list_metadata(self):
        start = parser.isoparse("2022-12-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")
        scope_filter = ScopeFilter(start=start, end=end)

        response = self.client.metadata.list_metadata(scope_filter)
        self.assertEqual(response.status_code, 200)

    def test_list_stream_names(self):
        start = parser.isoparse("2022-12-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")
        scope_filter = ScopeFilter(start=start, end=end)

        response = self.client.metadata.list_stream_names(scope_filter)
        self.assertEqual(response.status_code, 200)

    def test_devices_ids(self):
        start = parser.isoparse("2022-12-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")
        scope_filter = ScopeFilter(start=start, end=end)

        response = self.client.metadata.list_device_ids(scope_filter)
        self.assertEqual(response.status_code, 200)


unittest.main()
