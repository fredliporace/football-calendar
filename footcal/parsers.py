"""parsers module."""

from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone
from typing import List

import requests
from babel.dates import get_month_names
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from pydantic import BaseModel

from footcal import Match


class Parser(BaseModel, ABC):
    """A generic football fixture parser."""

    def get_matches(self, url: str) -> List[Match]:
        """Get matches from a given URL."""
        req = requests.get(url)
        if req.status_code != 200:
            raise RuntimeError(f"HTTP error {req.status_code}.")
        return self.matches_from_str(req.text)

    @staticmethod
    def _calendar_from_matches(calendar_name: str, matches: List[Match]) -> Calendar:
        """Build a calendar from a match list.

        Args:
          calendar_name: The calendar name.
          matches: List of matches.

        Returns:
          Calendar.
        """
        cal = Calendar()
        cal.add("name", calendar_name)
        for match in matches:
            event = Event()
            event.add("summary", f"{match.home_team} x {match.away_team}")
            if match.time_defined():
                event.add("dtstart", match.dt_start)
                event.add("dtend", match.dt_end)
            else:
                event.add("dtstart", match.dt_start.date())
            cal.add_component(event)
        return cal

    @abstractmethod
    def matches_from_str(self, html_text: str) -> List[Match]:
        """Get matches HTML str text."""


class ESPNParser(Parser):
    """Parser from ESPN fixture site."""

    # This is added to the schedule hour, may change depending
    # on your timzone
    delta_hour: int = 0
    # This is used to translate month abbreviated names (jan, fev, ...) to their
    # indexes (0, 1, ...)
    locale: str = "pt_BR"

    def matches_from_str(self, html_text: str) -> List[Match]:
        """todo: reference documentation from base class."""
        matches = []
        soup = BeautifulSoup(html_text, features="html.parser")
        for title in soup.find_all("div", "Table__Title"):
            # print(title.text)
            year = int(title.text.split(", ")[1])
            # print(year)
            trs = title.parent.find_all("tr")
            for tri in trs:
                tds = tri.find_all("td")
                if len(tds) == 7:
                    month = (
                        list(
                            get_month_names("abbreviated", locale=self.locale).values()
                        ).index(tds[0].text.split(" ")[2])
                        + 1
                    )
                    day = int(tds[0].text.split(" ")[1])
                    hour_minute = tds[4].text.split(":")
                    if len(hour_minute) != 2:
                        # No time defined yet, adding as a full day event
                        dt_start = datetime(year=year, month=month, day=day)
                        matches.append(
                            Match(
                                home_team=tds[1].text,
                                away_team=tds[3].text,
                                dt_start=dt_start,
                                comments=tds[5].text,
                            )
                        )

                    else:
                        dt_start = datetime(
                            year=year,
                            month=month,
                            day=day,
                            hour=int(hour_minute[0]) + self.delta_hour,
                            minute=int(hour_minute[1]),
                            # Obtaining local timezone: https://stackoverflow.com/a/39079819/1259982
                            tzinfo=datetime.now(timezone.utc).astimezone().tzinfo,
                        )
                        matches.append(
                            Match(
                                home_team=tds[1].text,
                                away_team=tds[3].text,
                                dt_start=dt_start,
                                dt_end=dt_start + timedelta(minutes=105),
                                comments=tds[5].text,
                            )
                        )
                    # print(f"\t{tds[0].text} {tds[1].text}
                    # {tds[3].text} {tds[4].text} {tds[5].text}")
                    # print(match)
        return matches
