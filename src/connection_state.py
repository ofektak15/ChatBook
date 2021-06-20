from enum import Enum


class ConnectionState(Enum):
    CLOSED = 1
    UNAUTHENTICATED = 2
    BROADCAST = 3
