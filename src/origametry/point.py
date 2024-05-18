from .constants import TOLERANCE
from .helpers import projection


class Point:

    """ A simple container class for Cartesian coordinates """

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __copy__(self):
        return Point(self._x, self._y)

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False

        return (
            abs(self._x - other.x) < TOLERANCE and
            abs(self._y - other.y) < TOLERANCE
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def isOn(self, line) -> bool:
        return self == projection(self, line)
