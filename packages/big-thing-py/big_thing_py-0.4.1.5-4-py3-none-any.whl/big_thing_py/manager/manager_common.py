from big_thing_py.utils import *
from enum import Enum, auto


class MXManagerMode(Enum):
    UNDEFINED = 'UNDEFINED'
    JOIN = 'JOIN'
    SPLIT = 'SPLIT'

    @classmethod
    def get(cls, name: str) -> 'MXManagerMode':
        try:
            return cls[name.upper()]
        except Exception:
            return cls.UNDEFINED


class MXStaffThingInfo:
    def __init__(self, staff_thing_id: str) -> None:
        self.staff_thing_id = staff_thing_id


class StaffRegisterResult:
    def __init__(self, staff_thing_name: str, staff_thing_id: str, assigned_staff_thing_id: str) -> None:
        self.staff_thing_name = staff_thing_name
        self.staff_thing_id = staff_thing_id
        self.assigned_staff_thing_id = assigned_staff_thing_id
