from enum import Enum

class Role(Enum):
    ADMIN = 1
    END_USER = 2
    SUPER_ADMIN = 3


class Gender(Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class PayType(Enum):
    CASH = 1
    CARD = 2
    ONLINE = 3

class PayStatus(Enum):
    PENDING = 1
    COMPLETE = 2
    FAILED = 3



