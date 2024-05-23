import numpy as np
import sympy
from math import inf, sqrt
from typing import Union, Optional, List
from multimethod import multimethod, DispatchError

from .line import Line
from .point import Point
from .reflect import reflect
from .helpers import (
    cast_to_real, remove_duplicates, midpoint, inverse, projection, distance,
    points_on_line,
)
from .constants import TOLERANCE

Creases = Optional[Union[Line, List[Line]]]


@multimethod
def _fold(p1: Point, q1: Point, p2: Point, q2: Point) -> Creases:
    """ axiom 1: crease through two points """

    # special case: all define the same point
    if p1 == q1 == p2 == q2:
        raise ValueError("Folding through a single point defines infinitely many creases")

    # expected case: two distinct points
    if p1 == q1 and p2 == q2:
        return Line(p1, p2)

    # undocumented case: point onto point with crease passing through a third point;
    # in certain cases this does define a line, so let's try
    if p1 == q1:
        # first get the crease that puts `p2` onto `q2`
        crease = _fold(p2, q2)

        # then check whether that line also goes through `p1`
        return crease if p1.isOn(crease) else None

    # ... and the mirror image
    if p2 == q2:
        crease = _fold(p1, q1)

        return crease if p2.isOn(crease) else None

    # undocumented case: 2 pairs of distinct points
    crease_1 = fold(p1, q1)
    crease_2 = fold(p2, q2)

    if crease_1 == crease_2:
        return crease_1


@multimethod
def _fold(p1: Point, p2: Point) -> Creases:
    """ axiom 2: point onto point """

    if p1 == p2:
        raise ValueError("Folding a point onto itself defines infinitely may creases")

    # the crease will be perpendicular to the line through `p1` and `p2`
    gradient = inverse(Line(p1, p2).gradient)

    return Line(midpoint(p1, p2), gradient)


@multimethod
def _fold(line_1: Line, line_2: Line) -> Creases:
    """ axiom 3: line onto line """

    # special case: line onto itself
    if line_1 == line_2:
        raise ValueError("Folding a line onto itself defines infinitely may creases")

    # special case: parallel lines
    if line_1.gradient == line_2.gradient:
        # find an arbitrary point on each of the lines
        p1 = next(points_on_line(line_1))
        p2 = next(points_on_line(line_2))

        # their midpoint will lie on the crease
        return Line(midpoint(p1, p2), line_1.gradient)

    # general case
    intersection = line_1.intersection(line_2)

    # there are two creases (perpendicular to each other) that satisfy the conditions
    # and they are given by the equation:
    # (a1.x + b1.y + c1) / sqrt(a1^2 + b1^2) = ± (a2.x + b2.y + c2) / sqrt(a2^2 + b2^2)

    # first take the positive case
    denominator_1 = sqrt(line_1.a ** 2 + line_1.b ** 2)
    denominator_2 = sqrt(line_2.a ** 2 + line_2.b ** 2)

    a = line_1.a * denominator_2 - line_2.a * denominator_1
    b = line_1.b * denominator_2 - line_2.b * denominator_1

    gradient = inf if b == 0 else -a / b

    # the negative case will be the perpendicular line through the `intersection`
    return (
        Line(intersection, gradient),
        Line(intersection, inverse(gradient))
    )


@multimethod
def _fold(p1: Point, p2: Point, line_1: Line, line_2: Line) -> Creases:
    """ axiom 4: through point and perpendicular to line """

    # expected case
    if p1 == p2 and line_1 == line_2:
        return Line(p1, inverse(line_1.gradient))

    # first undocumented case: point onto point with crease perpendicular to a line;
    # in certain cases this does define a line, so let's try
    if line_1 == line_2:
        # point onto a different point uniquely defines a crease
        crease: Line = _fold(p1, p2)

        # check whether that line also satisfies perpendicularity
        is_perpendicular = crease.gradient == inverse(line_1.gradient)

        return crease if is_perpendicular else None

    # second undocumented case: line onto line with crease through a point;
    # in certain cases this also defines one or more lines, so let's try
    if p1 == p2:
        # line onto a different line defines one or more creases
        creases: Union[Line, List[Line]] = _fold(line_1, line_2)

        # convert to a list of lines
        candidates: List[Line] = [creases] if isinstance(creases, Line) else creases

        # return only those which also go through the point
        solutions = list(filter(p1.isOn, candidates))

        if len(solutions) == 1:
            return solutions[0]
        if len(solutions) > 1:
            return solutions
        return None

    # final undocumented case: point onto point and line onto line;
    # even this could define a line, so let's try

    # get the crease defined by the two points
    crease: Line = _fold(p1, p2)

    # get the crease(s) defined by the two lines
    creases: Union[Line, List[Line]] = _fold(line_1, line_2)

    candidates: List[Line] = [creases] if isinstance(creases, Line) else creases

    # at most one of these will match the first crease
    for candidate in candidates:
        if candidate == crease:
            return crease


@multimethod
def _fold(line_1: Line, line_2: Line, p1: Point, p2: Point) -> Creases:
    """ alternative signature for axiom 4 """
    return _fold(p1, p2, line_1, line_2)


@multimethod
def _fold(p1: Point, line: Line, p2: Point, p3: Point) -> Creases:
    """ axiom 5: point onto line and through point """

    # trivial case
    if p1.isOn(line) and p2 == p3:
        raise ValueError("Point is already on the line, giving infinitely many creases")

    # trivial case
    if p1 == p2 == p3:
        return None

    # expected case
    if p2 == p3:
        # p1 will land on the line at a point equidistant from p2,
        # so consider a circle centred on p2 with the required radius
        radius = distance(p1, p2)

        # check that the circle actually does intersect the line
        p2_distance = distance(p2, line)

        if radius < p2_distance:
            # the fulcrum p2 is too far away from the line
            return None

        if radius == p2_distance:
            #  the line is tangent to the circle
            return fold(p1, projection(p2, line))

        # follow https://mathworld.wolfram.com/Circle-LineIntersection.html
        # we will assume the circle is centred on (0, 0) and then translate the
        # solutions by the coordinates of p2 at the end

        # get two points on the line
        line_point_1, line_point_2 = tuple(points_on_line(line, 2))

        # translate by the same amount as the circle
        line_point_1 = Point(line_point_1.x - p2.x, line_point_1.y - p2.y)
        line_point_2 = Point(line_point_2.x - p2.x, line_point_2.y - p2.y)

        # define some constants
        dx = line_point_2.x - line_point_1.x
        dy = line_point_2.y - line_point_1.y
        dr = distance(line_point_1, line_point_2)
        D = line_point_1.x * line_point_2.y - line_point_2.x * line_point_1.y
        sgn = -1 if dy < 0 else 1

        # root of the "discriminant"
        disc_root = sqrt(radius ** 2 * dr ** 2 - D ** 2)

        # solutions are given by
        x1 = (D * dy + sgn * dx * disc_root) / dr ** 2
        y1 = (-D * dx + abs(dy) * disc_root) / dr ** 2
        # and
        x2 = (D * dy - sgn * dx * disc_root) / dr ** 2
        y2 = (-D * dx - abs(dy) * disc_root) / dr ** 2

        return [
            fold(p1, Point(x1 + p2.x, y1 + p2.y)),
            fold(p1, Point(x2 + p2.x, y2 + p2.y))
        ]

    # undocumented case: point onto line and point onto point;
    # in certain cases this does define a line, so let's try
    if p2 != p3:
        # get the line putting p2 onto p3
        crease = fold(p2, p3)

        # check whether it also puts p1 onto the line
        if p1.isOn(line) or reflect(p1, crease).isOn(line):
            return crease


@multimethod
def _fold(line: Line, p1: Point, p2: Point, p3: Point) -> Creases:
    """ alternative signature for axiom 5 """
    return _fold(p1, line, p2, p3)


@multimethod
def _fold(p2: Point, p3: Point, p1: Point, line: Line) -> Creases:
    """ alternative signature for axiom 5 """
    return _fold(p1, line, p2, p3)


@multimethod
def _fold(p2: Point, p3: Point, line: Line, p1: Point) -> Creases:
    """ alternative signature for axiom 5 """
    return _fold(p1, line, p2, p3)


@multimethod
def _fold(p1: Point, line_1: Line, p2: Point, line_2: Line) -> Creases:
    """ axiom 6: point onto line and point onto line """

    # trivial cases
    if p1.isOn(line_1):
        raise ValueError("First point is already on its line, giving infinitely many creases")

    if p2.isOn(line_2):
        raise ValueError("Second point is already on its line, giving infinitely many creases")

    if p1 == p2 and line_1 == line_2:
        raise ValueError("Points and lines are identical, giving infinitely many creases")

    # expected case
    # each point-line pair are the focus and directrix of a unique parabola
    # solution folds are all lines which are tangent to both parabolas
    a, b, c = line_1.a, line_1.b, line_1.c

    # equation of parabola:
    # distance to point (p, q) == distance to line ax + by + c = 0 (both sides squared)
    # (x - p)^2 + (y - q)^2 = (a*x + b*y + c)^2 / (a^2 + b^2)
    # multiply out:
    # x^2 - 2*x*p + p^2 + y^2 - 2*y*q + q^2 = (a^2*x^2 + b^2*y^2 + c^2 + 2*a*x*b*y + 2*a*x*c + 2*b*y*c) / (a^2 + b^2)
    # let d = a^2 + b^2 and simplify:
    d = a ** 2 + b ** 2
    # b^2*x^2 + a^2*y^2 - 2*a*b*x*y - 2*(p*d + a*c)*x - 2*(q*d + b*c)*y + (p^2 + q^2)*d - c^2 = 0

    # write in general conic form:
    #             (   b^2      -a*b        -p*d-a*c    )   (x)
    # (x, y, 1) . (  -a*b       a^2        -q*d-b*c    ) . (y) = 0
    #             (-p*d-a*c  -q*d-b*c   d*p^2+d*q^2-c^2)   (1)
    M1 = np.array([
        [b ** 2, -a * b, -p1.x * d - a * c],
        [-a * b, a ** 2, -p1.y * d - b * c],
        [-p1.x * d - a * c, -p1.y * d - b * c, d * (p1.x ** 2 + p1.y ** 2) - c ** 2],
    ])

    # repeat for the second parabola
    a, b, c = line_2.a, line_2.b, line_2.c
    d = a ** 2 + b ** 2

    M2 = np.array([
        [b ** 2, -a * b, -p2.x * d - a * c],
        [-a * b, a ** 2, -p2.y * d - b * c],
        [-p2.x * d - a * c, -p2.y * d - b * c, d * (p2.x ** 2 + p2.y ** 2) - c ** 2],
    ])

    # we now find the "dual conics" of the two parabolas by taking the inverse matrices
    A1 = np.linalg.inv(M1)
    A2 = np.linalg.inv(M2)

    # round any floating point errors to zero
    A1 /= np.amax(A1)
    A2 /= np.amax(A2)

    for A in (A1, A2):
        for iy, ix in np.ndindex(A.shape):
            if abs(A[iy, ix]) < TOLERANCE:
                A[iy, ix] = 0

    # and then multiplying out the general conic form to get equations for the duals
    a, b, c = sympy.symbols("a b c", real=True)
    vec = np.array([a, b, c])

    dual_conic_1 = sympy.Eq(vec.dot(A1).dot(vec), 0)
    dual_conic_2 = sympy.Eq(vec.dot(A2).dot(vec), 0)

    # points of a dual conic correspond to tangent lines of the original and vice versa,
    # so common tangents to the parabolas correspond to intersections of the dual conics

    # use SymPy to solve the dual equations for these intersections:
    dual_intersections = sympy.solve([dual_conic_1, dual_conic_2], [a, b, c])

    solutions = cast_to_real([
        # solutions are correct to some scalar multiple; set remaining variables to 1
        tuple(x.subs({a: 1, b: 1, c: 1}) for x in s)
        for s in dual_intersections
    ])

    # the special case c = 0 may give more solutions for tangents through the origin
    special_vec = np.array([a, b, 0])

    special_dual_intersections = sympy.solve([
        sympy.Eq(special_vec.dot(A1).dot(special_vec), 0),
        sympy.Eq(special_vec.dot(A2).dot(special_vec), 0),
    ], [a, b])

    solutions += cast_to_real([
        tuple(x.subs({a: 1, b: 1}) for x in s) + (0,)
        for s in special_dual_intersections
    ])

    return remove_duplicates([
        Line(a, b, c)
        for a, b, c in solutions
        # ignore the solution (0, 0, 1), which represents the tangent at infinity
        if abs(a) > TOLERANCE or abs(b) > TOLERANCE
    ])


@multimethod
def _fold(p1: Point, line_1: Line, line_2: Line, p2: Point) -> Creases:
    """ alternative signature for axiom 6 """
    return _fold(p1, line_1, p2, line_2)


@multimethod
def _fold(line_1: Line, p1: Point, p2: Point, line_2: Line) -> Creases:
    """ alternative signature for axiom 6 """
    return _fold(p1, line_1, p2, line_2)


@multimethod
def _fold(line_1: Line, p1: Point, line_2: Line, p2: Point) -> Creases:
    """ alternative signature for axiom 6 """
    return _fold(p1, line_1, p2, line_2)


@multimethod
def _fold(p: Point, line_1: Line, line_2: Line, line_3: Line) -> Creases:
    """ axiom 7: point onto line and perpendicular to line """

    # expected case
    if line_2 == line_3:
        # trivial case
        if p.isOn(line_1):
            raise ValueError("Point is already on the line, giving infinitely many creases")

        # trivial case
        if line_1.gradient == line_2.gradient:
            return None

        # general case
        # first get the line through `p` that is parallel to `line_2`
        parallel = Line(p, line_2.gradient)

        # get the new line's intersection with line_1
        p2 = parallel.intersection(line_1)

        # the fold will be perpendicular through the midpoint
        return Line(midpoint(p, p2), inverse(line_2.gradient))

    # undocumented case: point onto line and line onto line;
    # in certain cases this does define a line, so let's try
    if line_2 != line_3:
        # get the line(s) putting line_2 onto line_3
        creases = fold(line_2, line_3)

        # convert to a list of lines
        candidates: List[Line] = [creases] if isinstance(creases, Line) else creases

        # return only those which also put the point onto line_1
        solutions = [
            crease
            for crease in candidates
            if p.isOn(line_1) or reflect(p, crease).isOn(line_1)
        ]

        if len(solutions) == 1:
            return solutions[0]
        if len(solutions) > 1:
            return solutions
        return None


@multimethod
def _fold(line_1: Line, p: Point, line_2: Line, line_3: Line) -> Creases:
    """ alternative signature for axiom 7 """
    return _fold(p, line_1, line_2, line_3)


@multimethod
def _fold(line_2: Line, line_3: Line, p: Point, line_1: Line) -> Creases:
    """ alternative signature for axiom 7 """
    return _fold(p, line_1, line_2, line_3)


@multimethod
def _fold(line_2: Line, line_3: Line, line_1: Line, p: Point) -> Creases:
    """ alternative signature for axiom 7 """
    return _fold(p, line_1, line_2, line_3)


def fold(*args):
    """ wrapper function for custom error handling """

    try:
        return _fold(*args)
    except DispatchError:
        types = tuple(type(arg).__name__ for arg in args)

        raise TypeError(f"'fold' cannot be applied with arguments {types}")
