"""HomeLINK utilities."""
from dateutil import parser

from .exceptions import ApiException, AuthException


def check_status(status):
    """Check status of the call."""
    if status == 401:
        raise AuthException(f"Authorization failed: {status}")
    if status != 200:
        raise ApiException(f"Error request failed: {status}")


def parse_date(in_date):
    """Parse the date."""
    return parser.parse(in_date) if in_date else None
