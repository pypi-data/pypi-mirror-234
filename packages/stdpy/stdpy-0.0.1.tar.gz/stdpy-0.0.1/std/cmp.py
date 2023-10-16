from abc import ABC
from enum import Enum

from .marker import Sized
from .option import Option

class PartialEq[Rhs](ABC):
    def __eq__(self, other: Rhs) -> bool:
        pass

    def __ne__(self, other: Rhs) -> bool:
        return not self == other


class Ordering(Enum):
    # An ordering where a compared value is less than another.
    Less = -1
    # An ordering where a compared value is equal to another.
    Equal = 0
    # An ordering where a compared value is greater than another.
    Greater = 1


class PartialOrd[Rhs: Sized](PartialEq[Rhs: Sized]):
    def partial_cmp(self, other: Rhs) -> Option[Ordering]:
        pass

    def __lt__(self, other: Rhs) -> bool:
        raise NotImplementedError

    def __le__(self, other: Rhs) -> bool:
        raise NotImplementedError

    def __gt__(self, other: Rhs) -> bool:
        raise NotImplementedError

    def __ge__(self, other: Rhs) -> bool:
        raise NotImplementedError
