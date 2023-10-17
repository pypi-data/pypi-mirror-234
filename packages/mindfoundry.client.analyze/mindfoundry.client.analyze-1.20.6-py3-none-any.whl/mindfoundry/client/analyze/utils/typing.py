import os
from typing import Union


class Unset:
    def __bool__(self) -> bool:
        return False


UNSET: Unset = Unset()


def is_unset(obj) -> bool:
    return isinstance(obj, Unset)


def is_set(obj) -> bool:
    return not is_unset(obj)


PathLike = Union[str, os.PathLike]
