import hashlib
from datetime import datetime

import certifi
from flask import abort, Flask, jsonify, request
import hmac
import logging
from os import environ
import ssl as ssl_lib
import yaml

app = Flask(__name__)
if environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

SLACK_CONFIG_KEY = "slack"
VERSION_NUMBER = "v0"

# TODO: Break out into utils
with open("secrets.yml", "r") as stream:
    config = yaml.safe_load(stream)
    if SLACK_CONFIG_KEY not in config:
        logger.error("Couldn't find slack creds. Aborting.")
        exit(1)
    slack_config = config.get(SLACK_CONFIG_KEY)
    if "signing_secret" not in slack_config:
        logger.error("Couldn't find signing secret. Aborting.")
        exit(1)
    signing_secret = slack_config.get("signing_secret").encode("utf-8")


def is_validate_request(req: request) -> bool:
    req_timestamp = req.headers.get("X-Slack-Request-Timestamp")
    if abs(int(datetime.now().timestamp()) - int(req_timestamp)) > 60 * 5:
        logger.error("This request is quite old. Could be a replay attack. Bailing.")
        abort(403)

    req_signature = req.headers.get("X-Slack-Signature")
    req_data = req.get_data().decode("utf-8")
    logger.debug("Request data:" + req_data)
    basestring = f"{VERSION_NUMBER}:{req_timestamp}:{req_data}".encode("utf-8")
    my_signature = (
        "v0=" + hmac.new(signing_secret, basestring, hashlib.sha256).hexdigest()
    )
    return hmac.compare_digest(my_signature, req_signature)


@app.route("/hello-world", methods=["POST"])
def hello_world():
    if is_validate_request(request):
        logger.debug("Received valid request from slack. Processing.")
        return jsonify(
            response_type="in_channel", text="GOOOAAAAAAL! :ice_hockey_stick_and_puck:",
        )
    else:
        logging.error("Request is improperly signed.")
        abort(403)


if __name__ == "__main__":
    app.run()
