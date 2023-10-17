from strenum import LowercaseStrEnum
from enum import auto


class DEPLOYMENT_EXECUTION_RULES(LowercaseStrEnum):

    """Enumeration for deployments execution rules."""

    ENDPOINT = auto()
    PERIODIC = auto()
