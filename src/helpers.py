from math import sqrt, inf

import src.line as Line
import src.point as Point
import src.constants as constants


def cast_sympy_to_real(solutions):
    """ remove imaginary floating-point errors and cast to floats """

    real_solutions = []

    for s in solutions:
        # cast SymPy expressions to built-in `complex` type
        complex_solution = tuple(complex(x) for x in s)

        # throw out any solutions with non-negligible imaginary components
        if all(abs(x.imag) < constants.TOLERANCE for x in complex_solution):
            real_solutions.append(tuple(x.real for x in complex_solution))

    return real_solutions


def remove_duplicates(elements):
    """ works with unhashable types """

    unique_elements = []

    for e in elements:
        is_unique = True

        for u in unique_elements:
            if e == u:
                is_unique = False

        if is_unique:
            unique_elements.append(e)

    return unique_elements


def midpoint(p1, p2):
    """ get the point halfway between two points """

    return Point.Point((p1.x + p2.x) / 2, (p1.y + p2.y) / 2)


def inverse(gradient: float) -> float:
    """ get the gradient of a line perpendicular to the gradient provided """

    # handle horizontal gradient
    if gradient == 0:
        return inf

    # handle vertical gradient (not really needed, but better to be explicit)
    if gradient == inf:
        return 0

    # general case
    return -1 / gradient


def projection(point, line):
    """ get the closest point on a line to the given point """

    # get the perpendicular line through the given point
    perpendicular = Line.Line(point, inverse(line.gradient))

    # find the intersection of both lines, which is the desired point
    return perpendicular.intersection(line)


def _distance_point_to_point(p1, p2) -> float:
    """ get the Euclidean straight-line distance between two points """

    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)


def _distance_point_to_line(p, line) -> float:
    """ get the shortest straight-line distance between a point and a line """

    return distance(p, projection(p, line))


def distance(thing_1, thing_2) -> float:
    if isinstance(thing_1, Point.Point) and isinstance(thing_2, Point.Point):
        return _distance_point_to_point(thing_1, thing_2)
    if isinstance(thing_1, Point.Point) and isinstance(thing_2, Line.Line):
        return _distance_point_to_line(thing_1, thing_2)
    if isinstance(thing_1, Line.Line) and isinstance(thing_2, Point.Point):
        return _distance_point_to_line(thing_2, thing_1)

    types = (type(thing_1).__name__, type(thing_2).__name__)

    raise TypeError(f"'distance' cannot be calculated for types {types}")


def points_on_line(line, n: int = inf):
    """ yield distinct points on the given line """

    # special case: line is vertical
    if line.gradient == inf:
        x_intercept = -line.c / line.a
        y = 0

        while y < n:
            yield Point.Point(x_intercept, y)
            y += 1

    else:
        # plug in `x = 0, 1, 2, ...` to get y-values for each point
        x = 0

        while x < n:
            yield Point.Point(x, -(line.a * x + line.c) / line.b)
            x += 1
