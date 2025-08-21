from enum import Enum


class Status(str, Enum):
    UP = "UP"
    DOWN = "DOWN"


class Environment(str, Enum):
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TEST = "test"
