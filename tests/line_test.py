import pytest
from math import inf
from copy import copy

from src.origametry.line import Line
from src.origametry.point import Point


""" create directly from coefficients of the general-form line equation """

def test_line_from_coefficients():
    line = Line(3, 2, 1)

    assert line.a == 3
    assert line.b == 2
    assert line.c == 1

def test_line_from_scaled_coefficients():
    line = Line(1, 2, 4)

    # coefficients should be scaled such that c=1
    assert line.a == .25
    assert line.b == .5
    assert line.c == 1

def test_line_from_partial_coefficients():
    line = Line(2, 1)

    assert line.a == 2
    assert line.b == 1
    assert line.c == 0

def test_line_from_partial_scaled_coefficients():
    line = Line(1, 2)

    # coefficients should be scaled such that b=1
    assert line.a == .5
    assert line.b == 1
    assert line.c == 0

def test_invalid_coefficients():
    with pytest.raises(ValueError):
        Line(0, 0, 1)

""" create from two distinct points """

def test_line_from_two_points():
    point_1 = Point(0, 0)
    point_2 = Point(1, 2)

    line = Line(point_1, point_2)

    assert line.a == -2
    assert line.b == 1
    assert line.c == 0

def test_horizontal_line_from_two_points():
    point_1 = Point(0, 0)
    point_2 = Point(1, 0)

    line = Line(point_1, point_2)

    assert line.a == 0
    assert line.b == 1
    assert line.c == 0

def test_vertical_line_from_two_points():
    point_1 = Point(0, 0)
    point_2 = Point(0, 1)

    line = Line(point_1, point_2)

    assert line.a == 1
    assert line.b == 0
    assert line.c == 0

def test_line_from_two_nondistinct_points():
    point_1 = Point(0, 0)
    point_2 = Point(0, 0)

    with pytest.raises(ValueError):
        Line(point_1, point_2)

""" create from point and gradient """

def test_line_from_point_and_gradient():
    point = Point(1, 1)

    line = Line(point, 2)

    assert line.a == -2
    assert line.b == 1
    assert line.c == 1

def test_line_through_origin_from_point_and_gradient():
    point = Point(1, 2)

    line = Line(point, 2)

    assert line.a == -2
    assert line.b == 1
    assert line.c == 0

def test_horizontal_line_from_point_and_gradient():
    point = Point(0, 1)

    line = Line(point, 0)

    assert line.a == 0
    assert line.b == -1
    assert line.c == 1

def test_horizontal_line_through_origin_from_point_and_gradient():
    point = Point(0, 0)

    line = Line(point, 0)

    assert line.a == 0
    assert line.b == 1
    assert line.c == 0

def test_vertical_line_from_point_and_gradient():
    point = Point(1, 0)

    line = Line(point, inf)

    assert line.a == -1
    assert line.b == 0
    assert line.c == 1

def test_vertical_line_through_origin_from_point_and_gradient():
    point = Point(0, 0)

    line = Line(point, inf)

    assert line.a == 1
    assert line.b == 0
    assert line.c == 0

""" create from gradient only (assumed through origin) """

def test_line_from_gradient():
    line = Line(2)

    assert line.a == -2
    assert line.b == 1
    assert line.c == 0

def test_horizontal_line_from_gradient():
    line = Line(0)

    assert line.a == 0
    assert line.b == 1
    assert line.c == 0

def test_vertical_line_from_gradient():
    line = Line(inf)

    assert line.a == 1
    assert line.b == 0
    assert line.c == 0

""" Line equality comparison """

def test_compare_lines_eq():
    line_1 = Line(-2, 1)

    point_1 = Point(0, 0)
    point_2 = Point(1, 2)
    line_2 = Line(point_1, point_2)

    assert line_1 == line_2

def test_compare_lines_almost_eq():
    line_1 = Line(-2, 1)

    nearly_0 = .4 - .3 - .1
    point_1 = Point(nearly_0, nearly_0)
    point_2 = Point(1, 2)
    line_2 = Line(point_1, point_2)

    # lines don't benefit from fuzzy matching
    assert line_1 != line_2

def test_compare_lines_neq():
    line_1 = Line(1, 0)

    point_1 = Point(0, 0)
    point_2 = Point(1, 2)
    line_2 = Line(point_1, point_2)

    assert line_1 != line_2

def test_compare_line_with_non_line():
    line = Line(1, 0)
    other = (Line(2, 1),)

    assert line != other

def test_compare_non_line_with_line():
    other = (Line(2, 1),)
    line = Line(1, 0)

    assert other != line

""" clone a Line """

def test_copy_line():
    line_1 = Line(1, 2)
    line_2 = copy(line_1)

    assert line_1 == line_2

""" calculate the gradient """

def test_positive_slope():
    point_1 = Point(1, 2)
    point_2 = Point(5, 8)

    line = Line(point_1, point_2)

    assert line.gradient == 1.5

def test_negative_slope():
    point_1 = Point(1, 8)
    point_2 = Point(5, 2)

    line = Line(point_1, point_2)

    assert line.gradient == -1.5

def test_horizontal():
    point_1 = Point(0, 0)
    point_2 = Point(1, 0)

    line = Line(point_1, point_2)

    assert line.gradient == 0

def test_vertical():
    point_1 = Point(0, 0)
    point_2 = Point(0, 1)

    line = Line(point_1, point_2)

    assert line.gradient == inf

""" `Line.intersection` implementation """

def test_intersection_with_another_line():
    point_1 = Point(0, 0)
    point_2 = Point(1, 0)
    line_1 = Line(point_1, point_2)

    point_3 = Point(2, 5)
    line_2 = Line(point_1, point_3)

    intersection = line_1.intersection(line_2)

    assert intersection == point_1

def test_parallel_lines():
    point_1 = Point(0, 2)
    point_2 = Point(1, 3)
    line_1 = Line(point_1, point_2)

    point_3 = Point(2, -6)
    point_4 = Point(3, -5)
    line_2 = Line(point_3, point_4)

    intersection = line_1.intersection(line_2)

    assert intersection == None

def test_this_line_vertical():
    point_1 = Point(0, 0)
    point_2 = Point(0, 1)
    line_1 = Line(point_1, point_2)

    point_3 = Point(2, 5)
    line_2 = Line(point_1, point_3)

    intersection = line_1.intersection(line_2)

    assert intersection == point_1

def test_other_line_vertical():
    point_1 = Point(0, 0)
    point_2 = Point(1, 0)
    line_1 = Line(point_1, point_2)

    point_3 = Point(0, 5)
    line_2 = Line(point_1, point_3)

    intersection = line_1.intersection(line_2)

    assert intersection == point_1
