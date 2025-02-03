from enum import Enum

class RemoteType(int, Enum):
    REMOTE = 0
    HYBRID = 1
    ONSITE = 2


class JobType(str, Enum):
    FULL_TIME = "full-time"
    PART_TIME = "part-time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
