from nylas_v3.handler.http_client import HttpClient


class Resource:
    """Base class for all Nylas API resources."""

    def __init__(self, http_client: HttpClient):
        self._http_client = http_client
