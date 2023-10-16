from enum import Enum


class InvalidContextError(Exception):
    pass


class ContextIn(Enum):
    SERVICEOWNER = "serviceowner"
    CONSUMER = "consumer"
