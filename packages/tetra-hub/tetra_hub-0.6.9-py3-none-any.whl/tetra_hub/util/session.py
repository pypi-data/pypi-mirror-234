import logging

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

MAX_RETRIES = 2


class LogRetry(Retry):
    """
    Adding extra logs before making a retry request
    """

    def __init__(self, total, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Total is the number of retries remaining. Starts at MAX_RETRIES and counts down to zero.
        if total < MAX_RETRIES:
            logging.info(f"Retry attempt number: {MAX_RETRIES - total}")


def create_session():
    session = requests.Session()
    retries = LogRetry(
        total=MAX_RETRIES,
        status_forcelist=[
            429,  # Too many requests
            500,  # Internal Server Error
            502,  # Bad Gateway
            503,  # Service Unavailable
            504,  # Gateway Timeout
        ],
    )

    session.mount("http://", HTTPAdapter(max_retries=retries))
    session.mount("https://", HTTPAdapter(max_retries=retries))

    return session
