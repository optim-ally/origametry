from math import inf
from typing import Union, Optional
from multimethod import multimethod

from .point import Point
from .constants import TOLERANCE

Number = Union[int, float]


class Line:

    """
    Definition of a straight line in the plane.
    We use the general form `ax + by + c = 0` to define a line. Since we can
    scale `a`, `b` and `c` by a constant to get the same line, we can always
    set either `c = 1` or `c = 0`

    Initialisation supports the following signatures:

    1. Coefficients of the general-form equation (default: c = 0)
        a: int|float, b: int|float, c: int|float|None

    2. Two distinct points
        p1: Point, p2: Point

    3. Point and gradient
        p: Point, gradient: int|float

    4. Just the gradient through the origin
        gradient: int|float
    """

    @multimethod
    def __init__(self, a: Number, b: Number, c: Number = 0):
        """ Method 1: coefficients passed in directly """

        if a == b == 0:
            raise ValueError('One of "a" or "b" must be non-zero')

        if c:
            self._a = a / c
            self._b = b / c
            self._c = 1

        # if `c == 0`, we may scale coefficients to get `b = 1` or `b = 0`
        elif b:
            self._a = a / b
            self._b = 1
            self._c = 0

        # if `b == c == 0`, the line is vertical through the origin
        else:
            self._a = 1
            self._b = 0
            self._c = 0

    @multimethod
    def __init__(self, p1: Point, p2: Point):
        """ Method 2: calculate coefficients from two points on the line """

        # confirm that the points are distinct
        if p1 == p2:
            raise ValueError('Points must be distinct to define a line')

        # check whether the line is vertical
        if p1.x == p2.x:
            return self.__init__(p1, inf)

        # check whether the line is horizontal
        if p1.y == p2.y:
            return self.__init__(p1, 0)

        # general case
        return self.__init__(p1, (p1.y - p2.y) / (p1.x - p2.x))

    @multimethod
    def __init__(self, p: Point, gradient: Number):
        """ Method 3: calculate coefficients from one point and the gradient """

        # check whether the line is vertical
        if gradient == inf:

            # special case: vertical through the origin
            if p.x == 0:
                self._a = 1
                self._b = 0
                self._c = 0

            # general vertical case
            else:
                self._a = -1 / p.x
                self._b = 0
                self._c = 1

        else:
            y_intercept = p.y - gradient * p.x

            # special case: line crosses the origin
            if y_intercept == 0:
                self._a = -gradient
                self._b = 1
                self._c = 0

            # general case
            else:
                self._a = gradient / y_intercept
                self._b = -1 / y_intercept
                self._c = 1

    @multimethod
    def __init__(self, gradient: Number):
        """ Method 4: using just the gradient through the origin """

        return self.__init__(Point(0, 0), gradient)

    def __copy__(self):
        return Line(self._a, self._b, self._c)

    def __eq__(self, other):
        """
        By the nature of infinite lines, a small error locally will generally
        result in arbitrarily large errors elsewhere, so matching "within a
        given tolerance" is not a well-defined operation.

        This error can manifest as exaggerated scaling of the coefficients
        `a`, `b` and `c`, making fuzzy comparison impractical in some cases.

        In practice, though, most lines can still be compared in this way since
        the lines will be "close enough" within the sensible folding area.
        """

        if not isinstance(other, Line):
            return False

        return (
            abs(self._a - other.a) < TOLERANCE and
            abs(self._b - other.b) < TOLERANCE and
            abs(self._c - other.c) < TOLERANCE
        )

    @property
    def a(self) -> Number:
        return self._a

    @property
    def b(self) -> Number:
        return self._b

    @property
    def c(self) -> Number:
        return self._c

    @property
    def gradient(self):

        """ calculate the gradient of the line, i.e. "rise over run" """

        # check whether the line is vertical
        if self._b == 0:
            return inf

        return -self._a / self._b

    def intersection(self, other) -> Optional[Point]:

        """ get the intersection point of two lines if it exists """

        # check whether the lines are parallel i.e. no solutions
        if self.gradient == other.gradient:
            return None

        x = y = None

        # check whether this line is vertical
        if self._b == 0:
            x = -self._c / self._a
            y = (other.a * self._c - self._a * other.c) / (self._a * other.b)

        # check whether the other line is vertical
        elif other.b == 0:
            x = -other.c / other.a
            y = (self._a * other.c - other.a * self._c) / (other.a * self._b)

        else:
            divisor = (other.gradient - self.gradient) * self._b * other.b

            x = (self._b * other.c - other.b * self._c) / divisor
            y = (other.a * self._c - self._a * other.c) / divisor

        return Point(x, y)
