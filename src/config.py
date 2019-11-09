import yaml
import logging

SLACK_CONFIG_KEY = "slack"
SIGNING_SECRET_KEY = "signing_secret"

logger = logging.getLogger(__name__)

with open("secrets.yml", "r") as stream:
    cfg = yaml.safe_load(stream)
    if SLACK_CONFIG_KEY not in cfg:
        logger.error("Couldn't find slack creds. Aborting.")
        exit(1)
    slack_cfg = cfg.get(SLACK_CONFIG_KEY)
    if SIGNING_SECRET_KEY not in slack_cfg:
        logger.error("Couldn't find signing secret. Aborting.")
        exit(1)
