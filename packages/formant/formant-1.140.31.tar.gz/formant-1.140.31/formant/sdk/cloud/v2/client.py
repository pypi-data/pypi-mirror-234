from .src.admin_api import AdminAPI
from .src.query_api import QueryAPI
from .src.ingest_api import IngestAPI
import os

DEFAULT_BASE_URL = "https://api.formant.io/v1"


class Client:
    def __init__(
        self,
        email: str = None,
        password: str = None,
        base_url: str = DEFAULT_BASE_URL,
    ):
        self._email = os.getenv("FORMANT_EMAIL") if email is None else email
        self._password = os.getenv("FORMANT_PASSWORD") if password is None else password
        if self._email is None:
            raise ValueError(
                "email argument missing and FORMANT_EMAIL environment variable not set!"
            )
        if self._password is None:
            raise ValueError(
                "password argument missing and FORMANT_PASSWORD environment variable not set"
            )
        self.admin = AdminAPI(
            email=self._email, password=self._password, base_url=base_url
        )
        self.query = QueryAPI(
            email=self._email, password=self._password, base_url=base_url
        )
        self.ingest = IngestAPI(
            email=self._email, password=self._password, base_url=base_url
        )
