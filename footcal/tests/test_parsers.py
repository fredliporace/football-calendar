"""test parsers."""
from datetime import datetime

import pytest

from footcal import Match
from footcal.parsers import ESPNParser, Parser

# protected access for testing purposes only
# pylint: disable=protected-access


def test_parser_calendar_from_matches() -> None:
    """test_parser_calendar_from_matches."""
    matches = [
        Match(
            home_team="Fluminense",
            away_team="Rio Cricket Athletic",
            dt_start=datetime(2015, 1, 1, 12, 30, 59, 0),
            dt_end=datetime(2015, 1, 1, 12, 30, 59, 0),
        ),
        Match(
            home_team="Fluminense",
            away_team="Rio Cricket Athletic",
            dt_start=datetime(2015, 1, 2),
        ),
    ]
    cal = Parser._calendar_from_matches(calendar_name="Fluminense", matches=matches)
    assert (
        cal.to_ical() == b"BEGIN:VCALENDAR\r\nNAME:Fluminense\r\n"
        b"BEGIN:VEVENT\r\nSUMMARY:Fluminense x Rio Cricket Athletic\r\n"
        b"DTSTART;VALUE=DATE-TIME:20150101T123059\r\nDTEND;"
        b"VALUE=DATE-TIME:20150101T123059\r\nEND:"
        b"VEVENT\r\nBEGIN:VEVENT\r\nSUMMARY:Fluminense x Rio Cricket Athletic\r\n"
        b"DTSTART;VALUE=DATE:20150102\r\nEND:VEVENT\r\nEND:VCALENDAR\r\n"
    )


def test_parser_subclasses() -> None:
    """test_parser_subclasses."""
    subclasses = Parser.__subclasses__()
    assert sorted([subclass.__name__ for subclass in subclasses]) == ["ESPNParser"]


def test_parser() -> None:
    """test_parser.

    This instantiates a concrete class but only test features from base class.
    """
    parser = ESPNParser()
    with pytest.raises(RuntimeError):
        parser.get_matches(url="http://google.com/error.html")


def test_espn_parser() -> None:
    """test_espn_parser."""
    espn = ESPNParser(utc_offset=-4)

    # Check last available format
    with open("footcal/tests/fixtures/espn_flu.html", encoding="utf-8") as fin:
        html_text = fin.read()
    matches = espn.matches_from_str(html_text=html_text)
    assert len(matches) == 32
    # The returned timezone may depend on where the test is executed,
    # if javascript page interpretation is enabled.
    # Removing tz check from test. The reference value was
    # "2022-05-26T20:30:00-04:00" originally
    assert matches[0].dt_start.isoformat()[:-6] == "2022-05-26T20:30:00"

    # Check current online format, test here is limited since it
    # is not guaranteed that there will be a match. Anyway this works
    # as a canary to flag format changes.
    test_url = "https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense"
    matches = espn.get_matches(url=test_url)
    assert len(matches) > 0

    calendar = espn.get_calendar(url=test_url, calendar_name="test")
    assert not calendar.is_empty()
    assert not calendar.is_broken
