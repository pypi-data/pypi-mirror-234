import unittest
from formant.sdk.cloud.v2.src.query_api import QueryAPI
from formant.sdk.cloud.v2.formant_query_api_client.models.interval_query import (
    IntervalQuery,
)
from formant.sdk.cloud.v2.formant_query_api_client.models.interval_query_interval import (
    IntervalQueryInterval,
)
import dateutil.parser as parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestPresence(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestPresence, self).__init__(*args, **kwargs)
        self.client = QueryAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_online(self):
        interval_query_interval = IntervalQueryInterval("minute")
        start = parser.isoparse("2022-12-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")
        interval_query = IntervalQuery(interval_query_interval, start, end)

        response = self.client.presence.count(interval_query)
        self.assertEqual(response.status_code, 200)


unittest.main()
