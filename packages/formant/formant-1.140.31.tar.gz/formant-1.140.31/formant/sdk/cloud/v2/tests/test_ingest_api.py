import unittest
from formant.sdk.cloud.v2.src.ingest_api import IngestAPI
from formant.sdk.cloud.v2.formant_ingest_api_client.models.ingestion_request import (
    IngestionRequest,
)
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestIngestion(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestIngestion, self).__init__(*args, **kwargs)
        self.client = IngestAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_post(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        tags = {}
        ingestion_request = IngestionRequest(device_id, tags)
        ingestion_request.add_numeric("test", 1)
        response = self.client.ingest.post(ingestion_request)
        self.assertEqual(response.status_code, 204)

    def test_post_all(self):
        device_id = "404e2d2c-f95f-41d8-bce1-915e314a6898"
        tags = {}

        ingestion_request_1 = IngestionRequest(device_id, tags)
        ingestion_request_1.add_numeric("test", 1)

        ingestion_request_2 = IngestionRequest(device_id, tags)
        ingestion_request_2.add_text("test_str", "str")

        ingestion_requests = [ingestion_request_1, ingestion_request_2]
        response = self.client.ingest.post_all(ingestion_requests)
        self.assertEqual(response.status_code, 204)


unittest.main()
