import os
from mlflow.tracking.request_header.abstract_request_header_provider import RequestHeaderProvider


class RefractRequestHeaderProvider(RequestHeaderProvider):
    """RequestHeaderProvider provided through plugin system"""

    def in_context(self):
        return True

    def request_headers(self):
        return {"X-Auth-Username": os.getenv("MOSAIC_ID",""),
                "X-Auth-UserId": os.getenv("MOSAIC_ID",""),
                "X-Auth-Email": os.getenv("EMAIL_ID", ""),
                "X-Project-Id": os.getenv("PROJECT_ID","")}
