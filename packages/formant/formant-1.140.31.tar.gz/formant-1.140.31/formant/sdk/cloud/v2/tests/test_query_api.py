import unittest
from formant.sdk.cloud.v2.src.query_api import QueryAPI
from formant.sdk.cloud.v2.formant_query_api_client.models.query import (
    Query,
    QueryTypesItem,
)
from formant.sdk.cloud.v2.formant_query_api_client.models.stream_data_points_item import (
    StreamDataPointsItem,
)
import dateutil.parser as parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestQueries(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestQueries, self).__init__(*args, **kwargs)
        self.client = QueryAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_query_numeric(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.NUMERIC]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)

        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.numeric, True)

    def test_query_text(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.TEXT]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.text, True)

    def test_query_bitset(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.BITSET]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)

        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.bitset, True)

    def test_query_localization(self):
        start = parser.isoparse("2022-10-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.LOCALIZATION]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.localization, True)

    def test_query_point_cloud(self):
        start = parser.isoparse("2022-08-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.POINT_CLOUD]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.point_cloud, True)

    def test_query_location(self):
        start = parser.isoparse("2022-06-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.LOCATION]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.location, True)

    def test_query_file(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.FILE]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.file, True)

    def test_query_health(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.HEALTH]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.health, True)

    def test_query_transform_tree(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.TRANSFORM_TREE]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.transform_tree, True)

    def test_query_battery(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.BATTERY]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.battery, True)

    def test_query_video(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.VIDEO]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.video, True)

    def test_query_numeric_set(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.NUMERIC_SET]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.numeric_set, True)

    def test_query_json(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.JSON]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.json, True)

    def test_query_image(self):
        start = parser.isoparse("2022-11-11T02:00:00.000Z")
        end = parser.isoparse("2022-12-11T02:02:00.000Z")

        types = [QueryTypesItem.IMAGE]
        query = Query(start=start, end=end, types=types, next_="true")
        result = self.client.queries.query(query=query)

        self.assertEqual(result.status_code, 200)
        stream_data_points_item = result.parsed.items[0].points[0]

        self.assertIsInstance(
            stream_data_points_item,
            StreamDataPointsItem,
            "not an instance of StreamDataPointsItem",
        )

        self.assertIsNotNone(stream_data_points_item.image, True)


unittest.main()
