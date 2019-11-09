from os import environ

from flask import abort, Flask, jsonify, request
import logging

from src.utils import is_validate_request

app = Flask(__name__)

if environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@app.route("/score", methods=["POST"])
def score():
    if is_validate_request(request):
        logger.debug("Received valid request from slack. Processing.")
        return jsonify(
            response_type="in_channel", text="GOOOAAAAAAL! :ice_hockey_stick_and_puck:",
        )
    else:
        logging.error("Request is improperly signed.")
        abort(403)


@app.route("/", methods=["GET"])
def health_check():
    return "MattyBot is alive and well."


if __name__ == "__main__":
    app.run()
