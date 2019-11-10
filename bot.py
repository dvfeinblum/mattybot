from os import environ

from flask import Flask, jsonify, request
import logging

from src.dynamo import get_standings
from src.utils import validate_request

app = Flask(__name__)

if environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@app.route("/score", methods=["POST"])
@validate_request
def score():
    return jsonify(
        response_type="in_channel", text="GOOOAAAAAAL! :ice_hockey_stick_and_puck:",
    )


@app.route("/standings", methods=["POST"])
@validate_request
def standings():
    return get_standings(request)


@app.route("/", methods=["GET"])
def health_check():
    return "MattyBot is alive and well."


if __name__ == "__main__":
    app.run()
