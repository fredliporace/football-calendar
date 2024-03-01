"""Template lambda code for footcal service."""

import json
import logging
import os
from typing import Any, Dict

from footcal.parsers import ESPNParser  # pylint: disable=unused-import

logging.getLogger("botocore.credentials").disabled = True
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(os.environ.get("LOGGER_LEVEL", "INFO"))


def handler(
    event: Any, context: Any  # pylint: disable=unused-argument
) -> Dict[str, Any]:
    """Lambda handler."""
    # Need to explicitly pass timezone, see #1
    LOGGER.info(os.environ["PARSER"])
    LOGGER.info(os.environ["PARSER_CTOR_ARGS"])
    LOGGER.info(os.environ["PARSER_GET_CALENDAR_ARGS"])
    parser_ctor = globals()[os.environ["PARSER"]]
    # parser = ESPNParser(timezone_id="US/Eastern", locale="pt_BR")
    parser = parser_ctor(**(json.loads(os.environ["PARSER_CTOR_ARGS"])))
    # calendar = parser.get_calendar(
    #     url="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense",
    #     calendar_name="Calendar",
    # )
    calendar = parser.get_calendar(
        **(json.loads(os.environ["PARSER_GET_CALENDAR_ARGS"]))
    )
    return {"statusCode": 200, "body": calendar.to_ical().decode("utf-8")}
