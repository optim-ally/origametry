from .helpers import projection, is_close


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
            is_close(self._x, other.x) and
            is_close(self._y, other.y)
        )

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def isOn(self, line) -> bool:
        return self == projection(self, line)
