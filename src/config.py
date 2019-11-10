import yaml
import logging

logger = logging.getLogger(__name__)

with open("conf.d/secrets.yml", "r") as stream:
    cfg = yaml.safe_load(stream)
    if not cfg.get("admin", {}).get("secret"):
        logger.error("Admin secret not found. Unsafe to boot.")
        exit(1)
    slack_cfg = cfg.get("slack")
    if not slack_cfg.get("signing_secret"):
        logger.error("Signing secret for slack not found. Unsafe to boot.")
        exit(1)
    aws_cfg = cfg.get("aws")
