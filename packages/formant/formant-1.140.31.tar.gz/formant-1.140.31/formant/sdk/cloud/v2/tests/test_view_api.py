import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import PartialView
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestViews(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestViews, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_get(self):
        view_id = "d1201530-a65e-4e6a-948a-6af0a368d4b3"
        result = self.client.views.get(view_id)
        self.assertEqual(result.status_code, 200)

    def test_get_all(self):
        result = self.client.views.get_all()
        self.assertEqual(result.status_code, 200)

    def test_patch(self):
        view_id = "d1201530-a65e-4e6a-948a-6af0a368d4b3"
        partial_view = PartialView(organization_id=self.client.organization_id)
        result = self.client.views.patch(view_id, partial_view)
        self.assertEqual(result.status_code, 200)


unittest.main()
