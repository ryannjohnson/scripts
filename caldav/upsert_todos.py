#!/usr/bin/env python3

"""
Adds tasks to a CalDAV todo list if they don't already exist.

```bash
$ export $(cat .env | xargs)
$ python3 upsert_todos.py "Wash dishes" "Do laundry"
```
"""

import caldav
from datetime import datetime, timedelta
import icalendar
import os
import platform
import random
import sys
from typing import List
from urllib.parse import quote


CALDAV_HOST = os.environ["CALDAV_HOST"]
CALDAV_PASSWORD = os.environ["CALDAV_PASSWORD"]
CALDAV_USER = os.environ["CALDAV_USER"]


def main():
    summaries_to_create = set([str(x) for x in sys.argv[1:]])

    caldav_url = "https://{user}:{password}@{host}".format(
        host=CALDAV_HOST, password=quote(CALDAV_PASSWORD), user=quote(CALDAV_USER)
    )

    calendar = require_single_calendar(caldav_url)

    for pending_todo in calendar.todos():
        vcalendar = icalendar.Todo.from_ical(pending_todo.data)
        for component in vcalendar.walk("vtodo"):
            summary = str(component.get("summary"))
            summaries_to_create.discard(summary)
            break

    for summary in summaries_to_create:
        todo_data = new_todo_data(summary)
        calendar.add_todo(todo_data)


def require_single_calendar(url: str) -> caldav.Calendar:
    client = caldav.DAVClient(url)
    calendars = client.principal().calendars()

    if len(calendars) == 0:
        raise Exception("no calendars found")

    if len(calendars) > 1:
        raise Exception(
            "{} calendars exist, no support for multiple calendars".format(
                len(calendars)
            )
        )

    calendar = calendars[0]

    return calendar


ICAL_DATE_FORMAT = "%Y%m%dT%H%M%SZ"


def new_todo_data(summary: str) -> str:
    clean_summary = summary.replace("\n", r"\n")
    now = datetime.utcnow().strftime(ICAL_DATE_FORMAT)
    nonce = "".join([random.choice("0123456789") for x in range(6)])
    host = platform.uname()[1]

    data = todo_template.format(host=host, nonce=nonce, now=now, summary=clean_summary)

    return data


# TODO: Make CATEGORIES controllable.
todo_template = """BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VTODO
UID:{now}-{nonce}@{host}
DTSTAMP:{now}
SUMMARY:{summary}
CATEGORIES:HABITS
STATUS:NEEDS-ACTION
END:VTODO
END:VCALENDAR"""


if __name__ == "__main__":
    main()
