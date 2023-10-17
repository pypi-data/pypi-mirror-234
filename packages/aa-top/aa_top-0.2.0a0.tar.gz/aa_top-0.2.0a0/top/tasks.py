from datetime import datetime

from celery import shared_task
from psutil import cpu_count, cpu_freq, cpu_percent, disk_usage, getloadavg

from django.contrib.auth.models import User
from django.db.models import Count

from allianceauth.eveonline.models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo,
)
from allianceauth.services.hooks import get_extension_logger
from allianceauth.utils.cache import get_redis_client
from esi.models import Token

from top.task_helpers import (
    diff_string, find_procs_by_name, get_redis_task_queue_by_tasks, last_value,
    meminfo, open_last_aatop_txt, save_aatop_txt, sql_space_used,
)

logger = get_extension_logger(__name__)


@shared_task()
def update_aa_top_txt():
    last_aatop_txt = open_last_aatop_txt()
    lines = []
    lines.append(f"{datetime.now().isoformat()}\n")
    mem_info = meminfo()
    lines.append(f"CPU: {cpu_percent(interval=0.1)}% \n")
    lines.append(f"Core Count: {cpu_count()}, Frequency:{cpu_freq().max if cpu_freq().max == '0' else cpu_freq().current}\n")
    lines.append(f"Load: {getloadavg()}\n")
    lines.append(
        f"Memory: {(mem_info['MemTotal'] - mem_info['MemAvailable']) / 1024 / 1024 :.2f}GB/{mem_info['MemTotal'] / 1024 / 1024 :.2f}GB\n")
    lines.append(f"Redis Memory: {get_redis_client().info()['used_memory_human']}\n")
    lines.append(f"SQL Memory: RSS {find_procs_by_name('mariadbd')[0].memory_info().rss / 1024 / 1024 / 1024 :.2f}GB VMS {find_procs_by_name('mariadbd')[0].memory_info().vms / 1024 / 1024 / 1024 :.2f}GB \n")
    lines.append(
        f"Disk Space: {disk_usage('/').used / 1024 / 1024 / 1024 :.2f}GB/{disk_usage('/').total / 1024 / 1024 / 1024 :.2f}GB\n")
    lines.append(f"DB Size: {sql_space_used() / 1024 :.2f} GB\n")
    lines.append("\n")
    lines.append("----Django Models----\n")
    characters = EveCharacter.objects.count()
    lines.append(diff_string(
        label="Characters",
        value=characters,
        diff=characters - last_value(last_aatop_txt, value="Characters")
    ))
    corporations = EveCorporationInfo.objects.count()
    lines.append(diff_string(
        label="Corporations",
        value=corporations,
        diff=corporations - last_value(last_aatop_txt, value="Corporations")
    ))
    alliances = EveAllianceInfo.objects.count()
    lines.append(diff_string(
        label="Alliances",
        value=alliances,
        diff=alliances - last_value(last_aatop_txt, value="Alliances")
    ))
    tokens = tokens = Token.objects.count()
    lines.append(diff_string(
        label="Tokens",
        value=tokens,
        diff=tokens - last_value(last_aatop_txt, value="Tokens")
    ))
    tokens_unique = tokens = Token.objects.all().aggregate(
        char_counts=Count('character_id', distinct=True))["char_counts"]
    lines.append(diff_string(
        label="Unique Tokens",
        value=tokens_unique,
        diff=tokens_unique - last_value(last_aatop_txt, value="Unique Tokens")
    ))
    users = User.objects.count()
    lines.append(diff_string(
        label="Users",
        value=users,
        diff=users - last_value(last_aatop_txt, value="Users")
    ))
    lines.append("\n")
    lines.append("----Celery Tasks in Queue----\n")
    task_queue = get_redis_task_queue_by_tasks()
    for task in task_queue:
        lines.append(diff_string(
            label=task,
            value=task_queue[task],
            diff=task_queue[task] - last_value(last_aatop_txt, value=task)
        ))

    save_aatop_txt(lines)

    # Thu 02 Dec 2021 10:34:52 AM UTC CPU:  50.3% Load:  7.04  Memory: 74.09G/125.71G  Redis: 12.27G  MongoDB: 106.38G/346.73G

    #           0  queueApiCheck                                   7,567  Successful ESI calls in last 5 minutes (-8)
    #           0  queueDiscord                                        0  Failed ESI calls in last 5 minutes
    #           0  queueInfo                                       3,530  Successful SSO calls in last 5 minutes (+16)
    #           0  queueItemIndex                                      0  Failed SSO calls in last 5 minutes
    #           0  queuePublish
    #           0  queueRedisQ                                         0  ESI Requests Cached
    #           0  queueSocial                                         0  ESI Requests Not Cached
    #           0  queueStats
    #           0  queueTopAllTime                                    35  Character KillLogs to check (+18)
    #          56  queueWars (-1)                                 28,494  Unique Character RefreshTokens
    #                                                                  9  Corporation KillLogs to check (+1)
    #           0  Kills remaining to be fetched.                  3,585  Unique Corporation RefreshTokens
    #           0  Kills remaining to be parsed.
    #         297  Kills parsed last hour                      3,131,509  Characters
    #  68,144,702  Total Kills (70.2%)                           523,202  Corporations
    #  97,076,353  Top killID                                     12,984  Alliances

    #       1,141  User requests in last 5 minutes (+1)            1.24b  Sponsored Killmails (inflated)
    #         326  Unique user IP's in last 5 minutes (+2)        77.78b  Wallet Balance

    #         358  API requests in last 5 minutes                      0  Load Counter
    #       1,147  Unique IPs in last 5 minutes                        0  Reinforced Mode
    #       8,459  Requests in last 5 minutes (-1)                     0  420'ed
    #                                                                  0  420 Prone
    #       4,396  Listening Websockets
