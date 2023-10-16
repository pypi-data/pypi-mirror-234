from enum import Enum


class ResponseType(Enum):
    """
    Enum that represents the two possible response types from the OSCAR EMR REST API.
    """

    JSON = 0
    XML = 1
    NONE = 2
