import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import Annotation
from datetime import datetime
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"


class TestAnnotations(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestAnnotations, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_get_annotation_list(self):
        result = self.client.annotations.list_templates()
        self.assertEqual(result.status_code, 200)

    def test_get_annotation_template(self):
        annotation_template_id = "d12707ed-9a78-4293-b11a-ad0ad75ad849"
        result = self.client.annotations.get_template(annotation_template_id)
        self.assertEqual(result.status_code, 200)

    def test_post_annotation(self):
        user_id = "408a7c6b-3b16-4667-a554-0fecc9d069dc"
        time = datetime.now()
        message = "Hello"
        annotation = Annotation(user_id=user_id, time=time, message=message)
        result = self.client.annotations.post(annotation)
        self.assertEqual(result.status_code, 201)


unittest.main()
