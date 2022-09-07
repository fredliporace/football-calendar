"""Lambda code for footcal service."""

from typing import Any, Dict

from footcal.parsers import ESPNParser


def handler(
    event: Any, context: Any  # pylint: disable=unused-argument
) -> Dict[str, Any]:
    """Lambda handler."""
    # Need to explicitly pass timezone, see #1
    parser = ESPNParser(delta_hour=4, locale="pt_BR")
    calendar = parser.get_calendar(
        url="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense",
        calendar_name="Calendar",
    )
    return {"statusCode": 200, "body": calendar.to_ical().decode("utf-8")}
