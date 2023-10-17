import unittest
from formant.sdk.cloud.v2.src.admin_api import AdminAPI
from formant.sdk.cloud.v2.formant_admin_api_client.models import (
    Command,
    CommandParameter,
    CommandQuery,
)
from dateutil import parser
import os

EMAIL = os.getenv("FORMANT_EMAIL")
PASSWORD = os.getenv("FORMANT_PASSWORD")
BASE_URL = "https://api.formant.io/v1"

DEVICE_ID = "4939f663-fbf9-4f60-b5ef-f2fd87c0452d"


class TestCommands(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(TestCommands, self).__init__(*args, **kwargs)
        self.client = AdminAPI(email=EMAIL, password=PASSWORD, base_url=BASE_URL)

    def test_create_command(self):
        command_name = "shell_script"
        scrubber_time = parser.parse("2014-11-03T19:38:34.203Z")
        parameter = CommandParameter(scrubber_time=scrubber_time)
        command = Command(
            device_id=DEVICE_ID,
            command=command_name,
            command_template_id="9cb194ba-80dc-4eca-8456-cdc5c9bdf345",
            parameter=parameter,
            organization_id=self.client.organization_id,
        )
        result = self.client.commands.create(command)

        self.assertEqual(result.status_code, 201)

    def test_query_commands(self):
        command_query = CommandQuery(device_id=DEVICE_ID)
        result = self.client.commands.query(command_query)
        self.assertEqual(result.status_code, 200)


unittest.main()
