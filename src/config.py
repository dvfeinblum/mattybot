import yaml
import logging

logger = logging.getLogger(__name__)

with open("conf.d/secrets.yml", "r") as stream:
    cfg = yaml.safe_load(stream)
    slack_cfg = cfg.get("slack")
    aws_cfg = cfg.get("aws")
