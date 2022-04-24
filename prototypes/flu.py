"""Prototype obtaining data from ESPN page and creating ICAL for Flu matches."""

from datetime import datetime, timedelta, timezone
from typing import Optional, List

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel
from babel.dates import get_month_names
from icalendar import Calendar, Event

class Match(BaseModel):
    """A match."""
    home_team: str
    away_team: str
    dt_start: datetime
    dt_end: datetime
    comments: Optional[str]


def get_matches(url: str) -> List[Match]:
    """Obtain matches by parsing URL."""
    matches = []
    req = requests.get(url)
    soup = BeautifulSoup(req.text, features="html.parser")
    for title in soup.find_all("div", "Table__Title"):
        # print(title.text)
        year = int(title.text.split(", ")[1])
        # print(year)
        trs = title.parent.find_all("tr")
        for tri in trs:
            tds = tri.find_all("td")
            if len(tds) == 7:
                month = list(get_month_names("abbreviated", locale="pt_BR").values()).index(tds[0].text.split(" ")[2]) + 1
                day = int(tds[0].text.split(" ")[1])
                hour_minute = tds[4].text.split(":")
                if len(hour_minute) != 2:
                    # No time defined yet, skipping for now.
                    continue
                # Text is one hour late, DST somewhere?
                dt_start=datetime(year=year, month=month, day=day, hour=int(hour_minute[0]) + 1,
                                  minute=int(hour_minute[1]),
                                  # Obtaining local timezone: https://stackoverflow.com/a/39079819/1259982
                                  tzinfo=datetime.now(timezone.utc).astimezone().tzinfo)
                matches.append(Match(home_team=tds[1].text, away_team=tds[3].text,
                                     dt_start=dt_start,
                                     dt_end=dt_start + timedelta(minutes=105),
                                     comments=tds[5].text))
                #print(f"\t{tds[0].text} {tds[1].text} {tds[3].text} {tds[4].text} {tds[5].text}")
                #print(match)
    return matches

def build_calendar(matches: List[Match]) -> Calendar:
    """Build calendar from matches."""
    cal = Calendar()
    cal.add("name", "Fluminense")
    for match in matches:
        event = Event()
        event.add("summary", f"{match.home_team} x {match.away_team}")
        event.add("dtstart", match.dt_start)
        event.add("dtend", match.dt_end)
        cal.add_component(event)
    return cal

if __name__ == "__main__":
    matches = get_matches(url="https://www.espn.com.br/futebol/time/calendario/_/id/3445/fluminense")
    print(matches)
    calendar = build_calendar(matches)
    with open("fluminense.ical", "w") as fp_ical:
        fp_ical.write(calendar.to_ical().decode("utf-8"))
