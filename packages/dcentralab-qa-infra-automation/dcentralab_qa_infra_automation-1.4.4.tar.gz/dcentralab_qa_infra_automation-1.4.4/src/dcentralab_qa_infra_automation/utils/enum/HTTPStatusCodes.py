import enum
"""
HTTP status codes enum 

@Author: Efrat Cohen
@Date: 02.2023
"""


class HTTPStatusCodes(enum.Enum):
    """
    http status code types
    """
    ok_200 = 200
    bad_request_400 = 400
    unauthorized_401 = 401
    not_found_404 = 404
    internal_server_error_500 = 500
    service_unavailable_503 = 503
