import calendar
import logging
import os
import re
import time
import traceback
from datetime import datetime
from datetime import time as dttime
from datetime import timedelta, timezone
from html import unescape
from typing import Optional

from discord import app_commands
from discord.ext import commands

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
dir_path = os.path.dirname(os.path.realpath(__file__))

def dprint(*args, **kwargs):
    """[DEBUG] stuff"""
    prefix = "[DEBUG]"
    logger.debug(prefix, *args, **kwargs)
    print(prefix, *args, **kwargs)

def gifalendar_seconds_until(hours:int=0, minutes:int=0, seconds:int=0, timezone=None):
    given_time = dttime(hours, minutes, seconds, tzinfo=timezone)
    now = datetime.now(tz=timezone)
    future_exec = datetime.combine(now, given_time)
    if (future_exec - now).days < 0:  # If we are past the execution, it will take place tomorrow
        future_exec = datetime.combine(now + timedelta(days=1), given_time) # days always >= 0

    return (future_exec - now).total_seconds()

def extract_time_from_string(time_str:str):
    return map(int, time_str.split(':'))

def get_timezone_offset():
    offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
    offset = offset / 60 / 60 * -1
    return offset

def get_timezone_name(hours:int):
    return timezone(timedelta(hours=hours))

def get_weekday(timezone=None):
    return (calendar.day_name[datetime.weekday(datetime.now(tz=timezone))]).lower()

def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:
        return check_time >= begin_time or check_time <= end_time
# Test case when range is between 10:30am and 4:30pm
# is_time_between(time(10,30), time(16,30))

# Test case when range is between 10:00pm and 4:00am
# is_time_between(time(22,0), time(4,00))

def format_time_ms(time: float = None):
    """
    time: ms :float:

    :returns:
    timefmt: :class:`str` in hh:mm:ss format
    """
    if time is None:
        time = 0

    time = int(time/1000)
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)

    timefmt = "{}{}{:02d}:{:02d}".format(
        hours if hours else "",
        ":" if hours else "00:",
        minutes,
        seconds
    )

    return timefmt

def format_time_seconds(time: float = None):
    """
    time: seconds :float:

    :returns:
    timefmt: :class:`str` in hh:mm:ss format
    """
    #sum(int(i) * 60**index for index, i in enumerate(timestamp.split(":")[::-1]))
    if time is None or time < 0:
        time = 0

    time = int(time)
    minutes, seconds = divmod(time, 60)
    hours, minutes = divmod(minutes, 60)

    timefmt = "{}{}{:02d}:{:02d}".format(
        hours if hours else "",
        ":" if hours else "00:",
        minutes,
        seconds
    )

    return timefmt

def refactor_time_seconds(time_str: str = None):
    return format_time_seconds(str_time_to_seconds(time_str))

def get_uptime(self, format: Optional[bool], current_time: Optional[float]):
    if format:
        if current_time: return format_time_seconds(current_time-self.up_time)
        return format_time_seconds(self.up_time)
    if current_time: return current_time-self.up_time
    return self.up_time

def str_time_to_seconds(timestamp: str):
    pattern = re.compile("\d+:\d+:\d+")
    reMatch = pattern.match(timestamp)
    if reMatch:
        return sum(int(i) * 60**index for index, i in enumerate(timestamp.split(":")[::-1]))
    return 0

def str_time_to_miliseconds(timestamp: str):
    pattern = re.compile("\d+:\d+:\d+")
    reMatch = pattern.match(timestamp)
    if reMatch:
        return sum(int(i) * 60**index for index, i in enumerate(timestamp.split(":")[::-1]))*1000
    return 0

def split_timestamp(timestamp: str):
    pattern = re.compile("\d+:\d+:\d+")
    reMatch = pattern.match(timestamp)
    if reMatch:
        return timestamp.split(":")[::1]
    return 0

async def cogs_manager(bot: commands.Bot, mode: str, cogs: list) -> None:
    for cog in cogs:
        #print(cog)
        try:
            if mode == "unload":
                await bot.unload_extension(cog)
            elif mode == "load":
                await bot.load_extension(cog)
            elif mode == "reload":
                await bot.reload_extension(cog)
            else:
                raise ValueError("Invalid mode.")
        except Exception as e:
            raise traceback.print_exc()

async def cogs_controller(bot: commands.Bot, mode: str, *, cog: str) -> None:
    try:
        if mode == "unload":
            await bot.unload_extension(cog)
        elif mode == "load":
            await bot.load_extension(cog)
        elif mode == "reload":
            await bot.reload_extension(cog)
        else:
            raise ValueError("Invalid mode.")
    except Exception as e:
        raise e


def cleanxml(content: str):
    """
    HUBRID &amp; The Racers Feat. Hunter Norton ->HUBRID & The Racers Feat. Hunter Norton
    """
    if content is not None:
        return unescape(content)


def generate_autocomplete(suggestdict: dict, current: str, keep_keys: Optional[bool]=None):
    # keep_keys: use key as result
    suggest = []
    if not current:
        for k,v in suggestdict:
            if keep_keys:
                suggest.append(app_commands.Choice(name=str(k), value=str(k)))
            else:
                suggest.append(app_commands.Choice(name=str(k), value=str(v)))
    else:
        for k,v in suggestdict:
            if current.lower() in k.lower():
                if keep_keys:
                    suggest.append(app_commands.Choice(name=str(k), value=str(k)))
                else:
                    suggest.append(app_commands.Choice(name=str(k), value=str(v)))

    return suggest

class Colours:
    blue = 0x0279FD
    twitter_blue = 0x1DA1F2
    bright_green = 0x01D277
    dark_green = 0x1F8B4C
    orange = 0xE67E22
    pink = 0xCF84E0
    purple = 0xB734EB
    soft_green = 0x68C290
    soft_orange = 0xF9CB54
    soft_red = 0xCD6D6D
    yellow = 0xF9F586
    python_blue = 0x4B8BBE
    python_yellow = 0xFFD43B
    grass_green = 0x66FF00
    gold = 0xE6C200

    easter_like_colours = [
        (255, 247, 0),
        (255, 255, 224),
        (0, 255, 127),
        (189, 252, 201),
        (255, 192, 203),
        (255, 160, 122),
        (181, 115, 220),
        (221, 160, 221),
        (200, 162, 200),
        (238, 130, 238),
        (135, 206, 235),
        (0, 204, 204),
        (64, 224, 208),
    ]