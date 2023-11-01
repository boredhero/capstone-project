import time
from datetime import datetime
from enum import Enum

import pytz

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Make me your metaclass to be a Singleton! It's *magic*
        """
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

def get_unix_timestamp() -> int:
    """
    Returns the current unix timestamp
    """
    return int(time.time())


def get_human_readable_time_with_timezone(unix_timestamp=None, timezone="America/New_York", time_string_format="%m-%d-%Y %H:%M:%S", now=False) -> str:
    """
    Get a human readable time with timezone.

    :param int unix_timestamp: UNIX timestamp
    :param str timezone: Timezone OPTIONAL: Default is "America/New_York"
    :param str time_string_format: OPTIONAL: Time string format. Default is "%m-%d-%Y %H:%M:%S"
    :param bool now: OPTIONAL: If True, return the current time. Default is False

    :returns str: Human readable time with timezone
    """
    if now is True:
        unix_timestamp = int(time.time())
    if unix_timestamp is None:
        unix_timestamp = int(time.time())
    local_tz = pytz.timezone(timezone)
    dt = datetime.fromtimestamp(int(unix_timestamp))
    local_dt = local_tz.localize(dt, is_dst=None)
    return local_dt.strftime(time_string_format)

class GameColors(Enum):
    """
    Tuple (r, g, b) definitions of colors for the game
    """
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
