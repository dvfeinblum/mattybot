from os import environ

from flask import Flask, jsonify, request
import logging

from src.dynamo import get_standings, put_data
from src.fetch_standings import get_raw_standings
from src.validators import validate_admin_request, validate_slack_request

app = Flask(__name__)

if environ.get("DEBUG"):
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


@app.route("/score", methods=["POST"])
@validate_slack_request
def score():
    return jsonify(
        response_type="in_channel", text="GOOOAAAAAAL! :ice_hockey_stick_and_puck:",
    )


@app.route("/standings", methods=["POST"])
@validate_slack_request
def standings():
    return get_standings(request)


@app.route("/", methods=["GET"])
def health_check():
    return "MattyBot is alive and well."


@app.route("/update_standings", methods=["GET"])
@validate_admin_request
def update_standings():
    raw_standings = get_raw_standings()
    put_data(raw_standings)
    return "Successfully updated standings in Dynamo."


if __name__ == "__main__":
    app.run()
