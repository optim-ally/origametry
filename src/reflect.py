from multimethod import multimethod

from .line import Line
from .point import Point
from .helpers import projection, points_on_line


@multimethod
def reflect(line: Line, crease: Line):
    """ get the reflection of a line across the given crease """

    # first find two distinct points on the line
    p1, p2 = tuple(points_on_line(line, 2))

    # reflect both of those points across the crease
    reflection_1 = reflect(p1, crease)
    reflection_2 = reflect(p2, crease)

    # get the line through the reflected points
    return Line(reflection_1, reflection_2)


@multimethod
def reflect(point: Point, crease: Line) -> Point:
    """ get the reflection of a point across the given crease """

    midpoint = projection(point, crease)

    x_offset = point.x - midpoint.x
    y_offset = point.y - midpoint.y

    return Point(point.x - 2 * x_offset, point.y - 2 * y_offset)
