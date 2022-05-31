"""Prototype obtaining data from ESPN page and creating ICAL for Flu matches."""

from datetime import datetime, timedelta, timezone
from typing import List, Optional

import requests
from babel.dates import get_month_names
from bs4 import BeautifulSoup
from icalendar import Calendar, Event
from pydantic import BaseModel


class Match(BaseModel):  # pylint: disable=too-few-public-methods
    """A match."""

    dt_start: datetime
    home_team: str
    away_team: str
    # If dt_end is not defined then we assume that the match day
    # is fixed but the time is not. This is included in the calendar
    # as a all day event.
    dt_end: Optional[datetime]
    comments: Optional[str]

    def time_defined(self) -> bool:
        """True if match has time defined, false if only the day is defined."""
        return self.dt_end is not None


def get_matches(url: str, delta_hour: int) -> List[Match]:
    """Obtain matches by parsing URL."""
    matches = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    for title in soup.find_all("div", "Table__Title"):
        # print(title.text)
        trs = title.parent.find_all("tr")
        year = int(title.text.split(", ")[1])
        # print(year)
        for tri in trs:
            tds = tri.find_all("td")
            if len(tds) == 7:
                day = int(tds[0].text.split(" ")[1])
                hour_minute = tds[4].text.split(":")
                month = (
                    list(get_month_names("abbreviated", locale="pt_BR").values()).index(
                        tds[0].text.split(" ")[2]
                    )
                    + 1
                )
                if len(hour_minute) != 2:
                    # No time defined yet, adding as a full day event
                    dt_start = datetime(year=year, month=month, day=day)
                    matches.append(
                        Match(
                            dt_start=dt_start,
                            home_team=tds[1].text,
                            away_team=tds[3].text,
                            comments=tds[5].text,
                        )
                    )

                else:
                    dt_start = datetime(
                        hour=int(hour_minute[0]) + delta_hour,
                        year=year,
                        month=month,
                        day=day,
                        minute=int(hour_minute[1]),
                        # Obtaining local timezone: https://stackoverflow.com/a/39079819/1259982
                        tzinfo=datetime.now(timezone.utc).astimezone().tzinfo,
                    )
                    matches.append(
                        Match(
                            dt_start=dt_start,
                            home_team=tds[1].text,
                            away_team=tds[3].text,
                            dt_end=dt_start + timedelta(minutes=105),
                            comments=tds[5].text,
                        )
                    )
                # print(f"\t{tds[0].text} {tds[1].text} {tds[3].text} {tds[4].text} {tds[5].text}")
                # print(match)
    return matches


def build_calendar(matches: List[Match]) -> Calendar:
    """Build calendar from matches."""
    cal = Calendar()
    cal.add("name", "Fluminense")
    for match in matches:
        event = Event()
        event.add("summary", f"{match.home_team} x {match.away_team}")
        if match.time_defined():
            event.add("dtend", match.dt_end)
            event.add("dtstart", match.dt_start)
        else:
            event.add("dtstart", match.dt_start.date())
        cal.add_component(event)
    # event = Event()
    # event.add("dtstart", date.today())
    # cal.add_component(event)
    return cal


if __name__ == "__main__":
    my_matches = get_matches(
        url="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense",
        delta_hour=1,
    )
    print(my_matches)
    calendar = build_calendar(my_matches)
    with open("fluminense.ics", "w", encoding="utf-8") as fp_ical:
        fp_ical.write(calendar.to_ical().decode("utf-8"))
