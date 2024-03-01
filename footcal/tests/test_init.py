"""footcal module tests."""

from datetime import datetime

from footcal import Match


def test_match() -> None:
    """test_match."""
    match = Match(
        home_team="Fluminense",
        away_team="Canto do Rio",
        dt_start=datetime(2015, 1, 1, 12, 30, 59, 0),
        dt_end=datetime(2015, 1, 1, 12, 30, 59, 0),
    )
    assert match.time_defined()
    match = Match(
        home_team="Fluminense",
        away_team="Canto do Rio",
        dt_start=datetime(2015, 1, 1, 12, 30, 59, 0),
    )
    assert not match.time_defined()
