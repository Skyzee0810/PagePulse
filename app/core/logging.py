import json
import logging
import sys
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
        }

        if hasattr(record, "request_id"):
            log_data["request_id"] = (
                record.request_id
            )

        if hasattr(record, "url"):
            log_data["url"] = record.url

        return json.dumps(log_data)


def configure_logging():
    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler(sys.stdout)

    handler.setFormatter(JsonFormatter())

    logger.handlers.clear()
    logger.addHandler(handler)