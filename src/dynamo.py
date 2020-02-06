import boto3
from collections import OrderedDict
from flask import jsonify, request, Response
from src.config import aws_cfg

dynamodb_resource = boto3.resource("dynamodb")
table = dynamodb_resource.Table(aws_cfg.get("dynamo", {}).get("bot_state_table"))


def parse_team_stats(stat_obj: dict) -> str:
    """
    Currently, individual team's stats look like this from Dynamo:

    "Hotshots": {
    "GA": "25",
    "GF": "27",
    "GP": "7",
    "L": "3",
    "OTL": "0",
    "PTS": "8",
    "SOL": "0",
    "T": "0",
    "W": "4"
  }

    we turn these into a nice human readable line.

    :param stat_obj: dict containing a team's stats
    :return: strified version of this data
    """
    line = ""
    for stat, val in stat_obj.items():
        line += f"{stat}: {val}\t"

    return line + "\n"


def parse_all_stats(stat_obj: dict) -> str:
    """
    Takes the current state returned from Dynamo and
    returns it as a text blob ready for slack.

    :param stat_obj: Dict containing all the standings
    :return: String that will be sent to Slack
    """
    return "\n".join(
        [f"*{team}*\n{parse_team_stats(stats)}" for team, stats in stat_obj.items()]
    )


def get_standings(req: request) -> Response:
    """
    Returns league standings information. If a valid team name is provided,
    only that team's data will be highlighted.

    :param req: request object from the slack
    :return: response body containing standings info.
    """
    team = req.form.get("text", "").title()
    standings = table.get_item(Key={"key": "teams"}).get("Item", None)

    if not standings:
        raise ValueError("Dynamo didn't return any data.")

    # We don't need this where we're goin'
    standings.pop("key")

    ordered_standings = OrderedDict(
        sorted(standings.items(), key=lambda kv: int(kv[1]["PTS"]), reverse=True)
    )

    if team in ordered_standings:
        team_stats = ordered_standings.get(team)
        text = f"Here are the rec league standings for the *{team}*:\n{parse_team_stats(team_stats)}"
    else:
        text = (
            f"Here are the rec league standings:\n{parse_all_stats(ordered_standings)}"
        )

    return jsonify(response_type="in_channel", text=text)


def put_data(raw_item: dict) -> None:
    """
    Puts python dicts into the bot_state_table in dynamo.

    :param raw_item: python dict containing your document
    """
    table.put_item(Item=raw_item)
