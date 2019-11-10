from datetime import datetime
from functools import wraps

from flask import abort, request
import hashlib
import hmac
import logging

from src.config import slack_cfg

VERSION_NUMBER = "v0"

logger = logging.getLogger(__name__)


def _is_valid_request(req: request) -> None:
    """
    This function ensures that the request we received came from Slack.
    Details on the algorithm here can be found at:
    https://api.slack.com/docs/verifying-requests-from-slack

    :param req: Flask request object
    :return: bool indicating whether or not the request is valid.
    """
    req_timestamp = req.headers.get("X-Slack-Request-Timestamp")
    if abs(int(datetime.now().timestamp()) - int(req_timestamp)) > 60 * 5:
        logger.error("This request is quite old. Could be a replay attack. Bailing.")
        abort(403)

    req_signature = req.headers.get("X-Slack-Signature")
    req_data = req.get_data().decode("utf-8")
    logger.debug("Request data:" + req_data)
    basestring = f"{VERSION_NUMBER}:{req_timestamp}:{req_data}".encode("utf-8")
    my_signature = (
        "v0="
        + hmac.new(
            slack_cfg.get("signing_secret").encode("utf-8"), basestring, hashlib.sha256,
        ).hexdigest()
    )
    if not hmac.compare_digest(my_signature, req_signature):
        logging.error("Request is improperly signed.")
        abort(403)


# decorator for the above functionality
def validate_request(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        _is_valid_request(request)
        return func(*args, **kwargs)

    return wrapper
