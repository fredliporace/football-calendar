"""football-calendar module."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Match(
    BaseModel, validate_assignment=True
):  # pylint: disable=too-few-public-methods
    """A match."""

    home_team: str
    away_team: str
    dt_start: datetime
    # If dt_end is not defined then we assume that the match day
    # is fixed but the time is not. This is included in the calendar
    # as a all day event.
    dt_end: Optional[datetime]
    comments: Optional[str]

    def time_defined(self) -> bool:
        """True if match has time defined, false if only the day is defined."""
        return self.dt_end is not None
