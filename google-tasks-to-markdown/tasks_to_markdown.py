#!/usr/bin/env python3

"""
The motivation for this script is to delegate all my standup meeting
announcements to my Google Tasks list.

Each day, I put in every indivisible unit of work I intend to do into my
Google Tasks. This takes the owness off my memory to keep track of what
I'm responsible for on an hourly basis.

As I complete tasks, I check them off in real time.

This script grabs two groups of data:

1.  All tasks I haven't completed yet.
2.  The most recent day's completed tasks.

These are converted into two markdown lists for me to easily paste into
Slack at the beginning of my day.

Next steps may include:

* Automatically send results to Slack.
* Automate the broadcast of my tasks to a cron job/schedule.
* Add my Google Calendar events into completed tasks.
"""

from datetime import datetime, timedelta
from dotenv import load_dotenv
import httplib2
import json
import math
from typing import List

from googleutils import build_google_tasks_resource


# Belong to tasks.
STATUS_COMPLETED = 'completed'
STATUS_NEEDS_ACTION = 'needsAction'

# Datetime format for google.
GOOGLE_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'


def main(tasklist_name='@default') -> str:
    """Broadcasts yesterday's completed tasks and today's new ones."""

    resource = build_google_tasks_resource()

    list_tasks_response = resource.tasks().list(tasklist=tasklist_name, showHidden=True).execute() # pylint: disable=E1101
    if 'items' not in list_tasks_response:
        raise Exception('no tasks exist')
    tasks = [
        x for x in list_tasks_response['items']
        if x.get('title')
    ]

    markdown_components: List(str) = list()

    yesterday_tasks = most_recent_day_of_completed_tasks(tasks)
    if yesterday_tasks:
        out = "Yesterday:\n\n"
        out += tasks_to_markdown_list(yesterday_tasks)
        markdown_components.append(out)

    outstanding_tasks = [x for x in tasks if x['status'] == STATUS_NEEDS_ACTION]
    if outstanding_tasks:
        out = "Today:\n\n"
        out += tasks_to_markdown_list(outstanding_tasks)
        markdown_components.append(out)

    return '\n\n'.join(markdown_components)


def most_recent_day_of_completed_tasks(tasks: List) -> List:
    completed_tasks = [x for x in tasks if x['status'] == STATUS_COMPLETED]
    if not completed_tasks:
        return []

    latest_task = sorted(completed_tasks, key=lambda x: x['completed'], reverse=True)[0]
    latest_day_starts_at = start_of_task_day(latest_task)

    return [
        x for x in completed_tasks
        if datetime.strptime(x['completed'], GOOGLE_DATETIME_FORMAT) >= latest_day_starts_at
    ]


def start_of_task_day(task) -> datetime:
    """Uses "now" as the point of reference for the beginning of a day."""
    completed_at = datetime.strptime(task['completed'], GOOGLE_DATETIME_FORMAT)

    now = datetime.utcnow()
    seconds_ago: float = (now - completed_at).total_seconds()
    days_ago = int(math.ceil(seconds_ago / 86400))
    time_ago = timedelta(days=days_ago)

    return now - time_ago


def tasks_to_markdown_list(tasks: List) -> str:
    list_items = list()
    for task in tasks:
        list_items.append('* {}'.format(task['title']))
    return '\n'.join(list_items)


if __name__ == '__main__':
    load_dotenv()
    print(main())
