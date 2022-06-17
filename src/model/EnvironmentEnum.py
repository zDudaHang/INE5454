from enum import Enum


class EnvironmentEnum(str, Enum):
    DEBUG = 'DEBUG',
    VERBOSE = 'VERBOSE'
    SELENIUM_TIME_TO_WAIT = 'SELENIUM_TIME_TO_WAIT'