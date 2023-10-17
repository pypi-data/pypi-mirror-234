from enum import Enum
from typing import List


class ExtendedEnum(Enum):
    @classmethod
    def get_list_of_all_values(cls):
        return cls.__members__.values()

    @classmethod
    def from_string(cls, s: str) -> Enum:
        for x in cls:
            if s == x.name:
                return x
        raise ValueError(f"cannot find value [{s}]")


def enum_type_to_list_str(e: Enum) -> List[str]:
    a = [x.name for x in e]  # type: ignore
    return a


def enum_value_to_str(ev: Enum) -> str:
    return ev.name


def str_to_enum_value(s, e: Enum) -> Enum:
    for x in type(e):
        if s == x.name:
            return x
    raise ValueError(f"cannot find value [{s}]")


def str_to_enum_int(s: str, e: Enum) -> int:
    for x in type(e):
        if s == x.name:
            return x.value
    raise ValueError(f"cannot find value [{s}]")


def enum_int_to_name(i: int, e: Enum) -> str:
    for x in type(e):
        if i == x.value:
            return x.name
    raise ValueError(f"cannot find value [{i}]")
