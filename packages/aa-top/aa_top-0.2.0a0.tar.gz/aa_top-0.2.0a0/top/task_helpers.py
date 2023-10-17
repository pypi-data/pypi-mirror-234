import json
import os
import re
from collections import Counter

import celery
import psutil
import redis

from django.apps import apps
from django.conf import settings
from django.db import connection

from allianceauth.services.hooks import get_extension_logger

logger = get_extension_logger(__name__)


def diff_string(label: str, value, diff: int = 0) -> str:
    if diff == 0:
        diff_substring = ""
    elif diff > 0:
        diff_substring = f"(+{diff})"
    else:
        diff_substring = diff
    return f"{label}: {value} {diff_substring}\n"


def open_last_aatop_txt() -> str:
    last_aatop_txt = ""
    with open('/var/www/myauth/static/top/aatop.txt') as f:
        for line in f.readlines():
            last_aatop_txt += line
    f.close()
    return last_aatop_txt


def last_value(last_aatop_txt: str, value: str) -> int:
    try:
        last_value_string = re.search(re.compile(
            f"\\n{value}: \\d+"), last_aatop_txt).group()
        last_value = re.search(re.compile("\\d+"), last_value_string).group()
    except Exception:
        return 0
    return int(last_value)


def save_aatop_txt(lines: list):
    if settings.DEBUG:
        with open(os.path.join(settings.STATICFILES_DIRS[0], "top", 'aatop.txt'), 'w') as f:
            f.writelines(lines)
    else:
        with open(os.path.join(settings.STATIC_ROOT, "top/", 'aatop.txt'), 'w') as f:
            f.writelines(lines)


def meminfo() -> dict:
    meminfo = {
        i.split()[0].rstrip(':'): int(i.split()[1]) for i in open('/proc/meminfo').readlines()}
    return meminfo


def django_apps_number() -> int:
    addons = len(list(apps.get_app_configs()))
    return addons


def get_redis_task_queue_by_tasks() -> Counter:
    DEFAULT_SEP = '\x06\x16'
    redis_client = redis.from_url(settings.BROKER_URL)
    task_queue_stats = Counter()
    priority_queues = celery.current_app.conf.broker_transport_options["priority_steps"]
    default_queue = redis_client.lrange('celery', 0, -1)
    for task in default_queue:
        task.decode
        task_name = json.loads(task)['headers']['task']
        task_queue_stats[task_name] += 1
    for priority in priority_queues:
        queue = redis_client.lrange(f'celery{DEFAULT_SEP}{priority}', 0, -1)
        for task in queue:
            task.decode
            task_name = json.loads(task)['headers']['task']
            task_queue_stats[task_name] += 1
    return task_queue_stats


def sql_space_used() -> int:
    with connection.cursor() as cursor:
        cursor.execute(
            """SELECT
            SUM(DATA_LENGTH + INDEX_LENGTH) AS "SIZE IN MB"
            FROM INFORMATION_SCHEMA.TABLES
            WHERE
            TABLE_SCHEMA = %s;""", [settings.DATABASES['default']["NAME"]]
        )
        row = cursor.fetchone()
        return int(row[0])


def find_procs_by_name(name):
    "Return a list of processes matching 'name'."
    ls = []
    for p in psutil.process_iter(['name']):
        if p.info['name'] == name:
            ls.append(p)
    return ls
