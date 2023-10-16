from typing import *
from typing_extensions import override
from termcolor import *
from abc import *
from enum import Enum, auto


EMPTY_JSON = {}
THREAD_TIME_OUT = 0.0001


class TimeFormat(Enum):
    DATETIME1 = '%Y-%m-%d %H:%M:%S'
    DATETIME2 = '%Y%m%d_%H%M%S'
    DATE = '%Y-%m-%d'
    TIME = '%H:%M:%S'
    UNIXTIME = 'unixtime'


class MXPrintMode(Enum):
    def _generate_next_value_(name: str, start, count, last_values):
        return name.lower()

    UNDEFINED = auto()
    FULL = auto()
    ABBR = auto()
    SKIP = auto()

    @classmethod
    def get(cls, name: str) -> 'MXPrintMode':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class Direction(Enum):
    PUBLISH = 'PUBLISH'
    RECEIVED = 'RECEIVED'


class PrintTag:
    # MQTT protocol
    GOOD = '[%-30s]' % colored('✔✔✔', 'green')
    DUP = '[%-30s]' % colored('DUP✔', 'green')
    ERROR = '[%-30s]' % colored('✖✖✖', 'red')

    CONNECT = '[%-30s]' % colored('-> CONNECT', 'blue')
    DISCONNECT = '[%-30s]' % colored('-> DISCONNECT', 'blue')

    SUBSCRIBE = '[%-30s]' % colored('-> SUBSCRIBE', 'white')
    UNSUBSCRIBE = '[%-30s]' % colored('-> UNSUBSCRIBE', 'white')
