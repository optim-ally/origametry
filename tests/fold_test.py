import pytest
import unittest
from math import sqrt, inf

from src.origametry.line import Line
from src.origametry.point import Point
from src.origametry.fold import fold

case = unittest.TestCase()


""" axiom 1: fold through two points """

def test_through_two_points():
    point_1 = Point(0, 0)
    point_2 = Point(1, 2)

    crease = fold(point_1, point_1, point_2, point_2)

    assert crease == Line(-2, 1, 0)

def test_vertical_through_two_points():
    point_1 = Point(0, 0)
    point_2 = Point(0, 2)

    crease = fold(point_1, point_1, point_2, point_2)

    assert crease == Line(1, 0, 0)

def test_horizontal_through_two_points():
    point_1 = Point(0, 0)
    point_2 = Point(2, 0)

    crease = fold(point_1, point_1, point_2, point_2)

    assert crease == Line(0, 1, 0)

def test_through_two_identical_points():
    point_1 = Point(2, 0)
    point_2 = Point(2, 0)

    with pytest.raises(ValueError):
        fold(point_1, point_1, point_2, point_2)

""" axiom 2: fold point onto point """

def test_point_onto_point():
    point_1 = Point(0, 0)
    point_2 = Point(2, 2)

    crease = fold(point_1, point_2)

    assert crease == Line(1, 1, -2)

def test_horizontal_point_onto_point():
    point_1 = Point(0, 0)
    point_2 = Point(2, 0)

    crease = fold(point_1, point_2)

    assert crease == Line(-1, 0, 1)

def test_vertical_point_onto_point():
    point_1 = Point(0, 0)
    point_2 = Point(0, 2)

    crease = fold(point_1, point_2)

    assert crease == Line(0, -1, 1)

def test_point_onto_it():
    point_1 = Point(0, 2)
    point_2 = Point(0, 2)

    with pytest.raises(ValueError):
        fold(point_1, point_2)

""" axiom 3: fold line onto line """

def test_line_onto_line():
    line_1 = Line(-2, 1, 0)
    line_2 = Line(1, 2, 1)

    creases = fold(line_1, line_2)

    case.assertCountEqual(creases, (
        Line(3, 1, 1),
        Line(-1, 3, 1),
    ))

def test_horizontal_line_onto_line():
    line_1 = Line(0, -1, 1)
    line_2 = Line(1, 1, 0)

    creases = fold(line_1, line_2)

    factor = 1 / sqrt(2)
    case.assertCountEqual(creases, (
        Line(factor, factor - 1, 1),
        Line(-factor, -factor - 1, 1),
    ))

def test_vertical_line_onto_line():
    line_1 = Line(-1, 0, 1)
    line_2 = Line(1, 1, 0)

    creases = fold(line_1, line_2)

    factor = 1 / sqrt(2)
    case.assertCountEqual(creases, (
        Line(factor - 1, factor, 1),
        Line(-factor - 1, -factor, 1),
    ))

def test_line_onto_horizontal_line():
    line_1 = Line(1, 1, 0)
    line_2 = Line(0, -1, 1)

    creases = fold(line_1, line_2)

    factor = 1 / sqrt(2)
    case.assertCountEqual(creases, (
        Line(factor, factor - 1, 1),
        Line(-factor, -factor - 1, 1),
    ))

def test_line_onto_vertical_line():
    line_1 = Line(1, 1, 0)
    line_2 = Line(-1, 0, 1)

    creases = fold(line_1, line_2)

    factor = 1 / sqrt(2)
    case.assertCountEqual(creases, (
        Line(factor - 1, factor, 1),
        Line(-factor - 1, -factor, 1),
    ))

def test_line_onto_parallel_line():
    line_1 = Line(-2, 1, 0)
    line_2 = Line(-1, .5, 1)

    crease = fold(line_1, line_2)

    assert crease == Line(-2, 1, 1)

def test_horizontal_line_onto_parallel_line():
    line_1 = Line(0, 1, 0)
    line_2 = Line(0, -.5, 1)

    crease = fold(line_1, line_2)

    assert crease == Line(0, -1, 1)

def test_vertical_line_onto_parallel_line():
    line_1 = Line(1, 0, 0)
    line_2 = Line(-.5, 0, 1)

    crease = fold(line_1, line_2)

    assert crease == Line(-1, 0, 1)

def test_line_onto_it():
    line_1 = Line(0, 2)
    line_2 = Line(0, 2)

    with pytest.raises(ValueError):
        fold(line_1, line_2)

""" axiom 4: fold through point and perpendicular to line """

def test_through_point_and_perpendicular_to_line():
    point = Point(0, 5)
    line = Line(-2, 1, 0)

    crease = fold(point, point, line, line)

    assert crease == Line(-.1, -.2, 1)

def test_perpendicular_to_line_and_through_point():
    point = Point(0, 5)
    line = Line(-2, 1, 0)

    crease = fold(line, line, point, point)

    assert crease == Line(-.1, -.2, 1)

# TODO: fully test axiom 4

""" axiom 5: fold point onto line and through point """

def test_point_onto_line_through_point():
    point_1 = Point(0, 5)
    line = Line(Point(2, 3), 1)
    point_2 = Point(0, 3)

    creases = fold(point_1, line, point_2, point_2)

    case.assertCountEqual(creases, (
        Line(point_2, 1),
        Line(point_2, 0),
    ))

def test_line_onto_point_through_point():
    line = Line(Point(2, 3), 1)
    point_1 = Point(0, 5)
    point_2 = Point(0, 3)

    creases = fold(line, point_1, point_2, point_2)

    case.assertCountEqual(creases, (
        Line(point_2, 1),
        Line(point_2, 0),
    ))

def test_through_point_and_point_onto_line():
    point_1 = Point(0, 3)
    point_2 = Point(0, 5)
    line = Line(Point(2, 3), 1)

    creases = fold(point_1, point_1, point_2, line)

    case.assertCountEqual(creases, (
        Line(point_1, 1),
        Line(point_1, 0),
    ))

def test_through_point_and_line_onto_point():
    point_1 = Point(0, 3)
    line = Line(Point(2, 3), 1)
    point_2 = Point(0, 5)

    creases = fold(point_1, point_1, line, point_2)

    case.assertCountEqual(creases, (
        Line(point_1, 1),
        Line(point_1, 0),
    ))

def test_point_onto_vertical_line_through_point():
    point_1 = Point(-2, 2)
    line = Line(inf)
    point_2 = Point(0, 2)

    creases = fold(point_1, line, point_2, point_2)

    case.assertCountEqual(creases, (
        Line(point_2, 1),
        Line(point_2, -1),
    ))

def test_single_solution():
    point_1 = Point(0, 2)
    line = Line(0)
    point_2 = Point(2, 2)

    crease = fold(point_1, line, point_2, point_2)

    assert crease == Line(point_2, 1)

def test_no_solutions():
    point_1 = Point(0, 2)
    line = Line(0)
    point_2 = Point(1, 2)

    creases = fold(point_1, line, point_2, point_2)

    assert creases is None

def test_no_solutions_points_equal():
    point_1 = Point(0, 2)
    line = Line(0)
    point_2 = Point(0, 2)

    creases = fold(point_1, line, point_2, point_2)

    assert creases is None

def test_point_already_on_line():
    point_1 = Point(2, 0)
    line = Line(0)
    point_2 = Point(1, 1)

    with pytest.raises(ValueError):
        fold(point_1, line, point_2, point_2)

""" axiom 6: fold point onto line and point onto line """

def test_point_onto_line_and_point_onto_line():
    point_1 = Point(-1, 0)
    line_1 = Line(Point(0, -1), 0)
    point_2 = Point(1, 0)
    line_2 = Line(Point(0, 1), 0)

    creases = fold(point_1, line_1, point_2, line_2)

    case.assertCountEqual(creases, (
        Line(1),
    ))

def test_point_onto_line_and_point_onto_line_multiple_solutions():
    # example taken from PyCon US 2024 presentation "Computational Origami"

    point_1 = Point(0, 0)
    line_1 = Line(Point(0, 2), 0)
    point_2 = Point(-3.5, 0.5)
    line_2 = Line(Point(-1.5, 0), inf)

    creases = fold(point_1, line_1, point_2, line_2)

    case.assertCountEqual(creases, (
        Line(Point(0.5, 1), -0.5),
        Line(Point(-1, 1), 1),
        Line(Point(-2, 1), 2),
    ))

def test_point_onto_line_and_line_onto_point():
    # example taken from https://math.stackexchange.com/questions/2428815
    # "The common tangent of two tilted parabolas"

    point_1 = Point(-1, 1)
    line_1 = Line(1, 1, 1)
    line_2 = Line(1, -1, 1)
    point_2 = Point(1, -1)

    creases = fold(point_1, line_1, line_2, point_2)

    case.assertCountEqual(creases, (
        Line(0, -2, 1),
        Line((-1 - sqrt(7)) / 2, (3 + sqrt(7)) / 2, 1),
        Line((-1 + sqrt(7)) / 2, (3 - sqrt(7)) / 2, 1),
    ))

def test_line_onto_point_and_point_onto_line_multiple_solutions():
    line_1 = Line(Point(0, 2), 0)
    point_1 = Point(0, 0)
    point_2 = Point(-3.5, 0.5)
    line_2 = Line(Point(-1.5, 0), inf)

    creases = fold(line_1, point_1, point_2, line_2)

    case.assertCountEqual(creases, (
        Line(Point(0.5, 1), -0.5),
        Line(Point(-1, 1), 1),
        Line(Point(-2, 1), 2),
    ))

def test_line_onto_point_and_line_onto_point():
    line_1 = Line(1, 1, 1)
    point_1 = Point(-1, 1)
    line_2 = Line(1, -1, 1)
    point_2 = Point(1, -1)

    creases = fold(line_1, point_1, line_2, point_2)

    case.assertCountEqual(creases, (
        Line(0, -2, 1),
        Line((-1 - sqrt(7)) / 2, (3 + sqrt(7)) / 2, 1),
        Line((-1 + sqrt(7)) / 2, (3 - sqrt(7)) / 2, 1),
    ))

def test_two_points_onto_line():
    point_1 = Point(0, 3)
    point_2 = Point(0, 1)
    line = Line(Point(0, 2), 0)

    creases = fold(point_1, line, point_2, line)

    case.assertCountEqual(creases, (
        Line(Point(0, 2), 1),
        Line(Point(0, 2), -1),
    ))

def test_point_onto_two_lines():
    point = Point(0, 1)
    line_1 = Line(Point(0, 3), 1)
    line_2 = Line(Point(0, 3), -1)

    creases = fold(point, line_1, point, line_2)

    case.assertCountEqual(creases, (
        Line(Point(0, 2), 0),
    ))

def test_point_onto_two_parallel_lines():
    point = Point(0, 1)
    line_1 = Line(Point(1, 0), inf)
    line_2 = Line(Point(-1, 0), inf)

    creases = fold(point, line_1, point, line_2)

    assert creases == []

def test_through_origin_two_points_onto_line():
    point_1 = Point(0, 1)
    point_2 = Point(0, -1)
    line = Line(0)

    creases = fold(point_1, line, point_2, line)

    case.assertCountEqual(creases, (
        Line(1),
        Line(-1),
    ))

def test_opposite_points_on_parallel_lines():
    point_1 = Point(-1, 1)
    point_2 = Point(1, -1)
    line_1 = Line(point_2, 1)
    line_2 = Line(point_1, 1)

    creases = fold(point_1, line_1, point_2, line_2)

    case.assertCountEqual(creases, (
        Line(1),
    ))

def test_opposite_points_on_parallel_horizontal_lines():
    point_1 = Point(0, 1)
    point_2 = Point(0, -1)
    line_1 = Line(point_2, 0)
    line_2 = Line(point_1, 0)

    creases = fold(point_1, line_1, point_2, line_2)

    case.assertCountEqual(creases, (
        Line(0),
    ))

def test_opposite_points_on_parallel_vertical_lines():
    point_1 = Point(-1, 0)
    point_2 = Point(1, 0)
    line_1 = Line(point_2, inf)
    line_2 = Line(point_1, inf)

    creases = fold(point_1, line_1, point_2, line_2)

    case.assertCountEqual(creases, (
        Line(inf),
    ))

def test_point_onto_line_and_point_onto_line_no_solutions_1():
    # parabolas intersect and have opposite orientation
    point_1 = Point(0, 0)
    line_1 = Line(Point(0, -1), 0)
    point_2 = Point(0, 1)
    line_2 = Line(Point(0, 2), 0)

    creases = fold(point_1, line_1, point_2, line_2)

    assert creases == []

def test_point_onto_line_and_point_onto_line_no_solutions_2():
    # parabolas have same orientation and do not intersect
    point_1 = Point(0, 0)
    line_1 = Line(Point(0, 11), 0)
    point_2 = Point(0, 2)
    line_2 = Line(Point(0, 3), 0)

    creases = fold(point_1, line_1, point_2, line_2)

    assert creases == []

def test_point_already_on_line_and_point_onto_line():
    point_1 = Point(0, 0)
    line_1 = Line(Point(0, 0), 0)
    point_2 = Point(0, 1)
    line_2 = Line(Point(0, 2), 0)

    with pytest.raises(ValueError):
        fold(point_1, line_1, point_2, line_2)

def test_point_onto_line_and_point_already_on_line():
    point_1 = Point(0, 0)
    line_1 = Line(Point(0, -1), 0)
    point_2 = Point(0, 1)
    line_2 = Line(Point(0, 1), 0)

    with pytest.raises(ValueError):
        fold(point_1, line_1, point_2, line_2)

def test_same_point_onto_same_line_twice():
    point = Point(0, 0)
    line = Line(Point(0, -1), 0)

    with pytest.raises(ValueError):
        fold(point, line, point, line)

""" axiom 7: point onto line and perpendicular to line """

def test_point_onto_line_and_perpendicular_to_line():
    point = Point(0, 0)
    line_1 = Line(1, 0, -1)
    line_2 = Line(Point(3.14, -1729), 1)

    crease = fold(point, line_1, line_2, line_2)

    assert crease == Line(1, 1, -1)

def test_line_onto_point_and_perpendicular_to_line():
    line_1 = Line(1, 0, -1)
    point = Point(0, 0)
    line_2 = Line(Point(3.14, -1729), 1)

    crease = fold(line_1, point, line_2, line_2)

    assert crease == Line(1, 1, -1)

def test_perpendicular_to_line_and_point_onto_line():
    line_1 = Line(Point(3.14, -1729), 1)
    point = Point(0, 0)
    line_2 = Line(1, 0, -1)

    crease = fold(line_1, line_1, point, line_2)

    assert crease == Line(1, 1, -1)

def test_perpendicular_to_line_and_line_onto_point():
    line_1 = Line(Point(3.14, -1729), 1)
    line_2 = Line(1, 0, -1)
    point = Point(0, 0)

    crease = fold(line_1, line_1, line_2, point)

    assert crease == Line(1, 1, -1)

def test_point_onto_line_and_perpendicular_to_parallel_line():
    point = Point(0, 0)
    line_1 = Line(1, 0, -1)
    line_2 = Line(1, 0, 1)

    crease = fold(point, line_1, line_2, line_2)

    assert crease is None

def test_point_already_on_line_and_perpendicular_to_line():
    point = Point(1, 0)
    line_1 = Line(1, 0, -1)
    line_2 = Line(Point(3.14, -1729), 1)

    with pytest.raises(ValueError):
        fold(point, line_1, line_2, line_2)

""" undocumented cases """

def test_point_onto_point_and_through_point():
    point_1 = Point(0, 0)
    point_2 = Point(0, 2)
    point_3 = Point(4, 1)

    crease = fold(point_1, point_2, point_3, point_3)

    assert crease == Line(0, 1, -1)

def test_through_point_and_point_onto_point():
    point_1 = Point(4, 1)
    point_2 = Point(0, 0)
    point_3 = Point(0, 2)

    crease = fold(point_1, point_1, point_2, point_3)

    assert crease == Line(0, 1, -1)

def test_point_onto_point_and_through_point_no_solutions():
    point_1 = Point(0, 0)
    point_2 = Point(0, 2)
    point_3 = Point(4, 0)

    crease = fold(point_1, point_2, point_3, point_3)

    assert crease is None

def test_point_onto_point_and_point_onto_point():
    point_1 = Point(0, 0)
    point_2 = Point(0, 2)
    point_3 = Point(5, 0)
    point_4 = Point(5, 2)

    crease = fold(point_1, point_2, point_3, point_4)

    assert crease == Line(0, 1, -1)

def test_point_onto_point_and_point_onto_point_no_solutions():
    point_1 = Point(0, 0)
    point_2 = Point(0, 2)
    point_3 = Point(5, 0)
    point_4 = Point(6, 0)

    crease = fold(point_1, point_2, point_3, point_4)

    assert crease is None

def test_point_onto_point_perpendicular_to_line():
    point_1 = Point(1, 0)
    point_2 = Point(3, 2)
    line = Line(1)

    crease = fold(point_1, point_2, line, line)

    assert crease == Line(Point(2, 1), -1)

def test_point_onto_point_perpendicular_to_line_no_solutions():
    point_1 = Point(1, 0)
    point_2 = Point(3, 2)
    line = Line(-1)

    crease = fold(point_1, point_2, line, line)

    assert crease is None

def test_line_onto_line_and_through_point():
    line_1 = Line(0)
    line_2 = Line(inf)
    point = Point(1, 1)

    crease = fold(line_1, line_2, point, point)

    assert crease == Line(1)

def test_line_onto_line_and_through_point_multiple_solutions():
    line_1 = Line(0)
    line_2 = Line(inf)
    point = Point(0, 0)

    creases = fold(line_1, line_2, point, point)

    case.assertCountEqual(creases, (
        Line(1),
        Line(-1),
    ))

def test_line_onto_line_and_through_point_no_solutions():
    line_1 = Line(0)
    line_2 = Line(inf)
    point = Point(0, 1)

    crease = fold(line_1, line_2, point, point)

    assert crease is None

def test_line_onto_parallel_line_and_through_point():
    line_1 = Line(1, 0, 0)
    line_2 = Line(1, 0, -2)
    point = Point(1, 1)

    crease = fold(line_1, line_2, point, point)

    assert crease == Line(1, 0, -1)

def test_line_onto_parallel_line_and_through_point_no_solutions():
    line_1 = Line(1, 0, 0)
    line_2 = Line(1, 0, -2)
    point = Point(0, 1)

    crease = fold(line_1, line_2, point, point)

    assert crease is None

def test_point_onto_point_and_line_onto_line():
    point_1 = Point(2, 1)
    point_2 = Point(1, 2)
    line_1 = Line(0)
    line_2 = Line(inf)

    crease = fold(point_1, point_2, line_1, line_2)

    assert crease == Line(1)

def test_point_onto_point_and_line_onto_parallel_line():
    point_1 = Point(2, 1)
    point_2 = Point(2, 3)
    line_1 = Line(0, 1, 0)
    line_2 = Line(0, 1, -4)

    crease = fold(point_1, point_2, line_1, line_2)

    assert crease == Line(0, 1, -2)

def test_point_onto_point_and_line_onto_line_no_solutions():
    point_1 = Point(0, 0)
    point_2 = Point(1, 2)
    line_1 = Line(0)
    line_2 = Line(inf)

    crease = fold(point_1, point_2, line_1, line_2)

    assert crease is None

def test_point_onto_line_and_point_onto_point():
    point_1 = Point(1, 2)
    line = Line(0)
    point_2 = Point(5, -1)
    point_3 = Point(5, 3)

    crease = fold(point_1, line, point_2, point_3)

    assert crease == Line(0, 1, -1)

def test_point_onto_line_and_point_onto_point_no_solutions():
    point_1 = Point(1, 2)
    line = Line(0)
    point_2 = Point(5, -1)
    point_3 = Point(0, 3)

    crease = fold(point_1, line, point_2, point_3)

    assert crease is None

def test_point_onto_line_and_line_onto_line():
    point_1 = Point(2, 1)
    line_1 = Line(Point(1, 2), 5)
    line_2 = Line(0)
    line_3 = Line(inf)

    crease = fold(point_1, line_1, line_2, line_3)

    assert crease == Line(1)

def test_point_onto_line_and_line_onto_parallel_line():
    point_1 = Point(1, 2)
    line_1 = Line(0)
    line_2 = Line(0, 1, 1)
    line_3 = Line(0, 1, -3)

    crease = fold(point_1, line_1, line_2, line_3)

    assert crease == Line(0, 1, -1)

def test_point_already_on_line_and_line_onto_line():
    point_1 = Point(1, 0)
    line_1 = Line(0)
    line_2 = Line(0)
    line_3 = Line(inf)

    creases = fold(point_1, line_1, line_2, line_3)

    case.assertCountEqual(creases, (
        Line(1),
        Line(-1),
    ))

def test_point_onto_line_and_line_onto_line_no_solutions():
    point_1 = Point(2, 1)
    line_1 = Line(Point(1, 3), 5)
    line_2 = Line(0)
    line_3 = Line(inf)

    crease = fold(point_1, line_1, line_2, line_3)

    assert crease is None

""" bad input shape """

def test_single_argument():
    point = Point(0, 5)

    with pytest.raises(TypeError):
        fold(point)

def test_odd_number_of_arguments():
    point = Point(0, 5)
    line_1 = Line(0, 2)
    line_2 = Line(1, 3)

    with pytest.raises(TypeError):
        fold(point, line_1, line_2)

def test_unsupported_perpendicular_to_two_lines():
    line_1 = Line(0, 2)
    line_2 = Line(1, 3)

    with pytest.raises(TypeError):
        fold(line_1, line_1, line_2, line_2)
