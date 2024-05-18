from copy import copy

from src.origametry.line import Line
from src.origametry.point import Point


""" create directly from coefficients """

def test_create_point():
    point = Point(0, 0)

    assert point.x == 0
    assert point.y == 0

""" Point equality comparison """

def test_compare_points_eq():
    point_1 = Point(0, 0)
    point_2 = Point(0, 0)

    assert point_1 == point_2

def test_compare_points_almost_eq():
    nearly_0 = .4 - .3 - .1
    point_1 = Point(0, 0)
    point_2 = Point(nearly_0, -nearly_0)

    # points don't exactly align due to floating-point error...
    assert point_1.y != point_2.y
    assert point_1.x != point_2.x

    # ... but they compare equal anyway
    assert point_1 == point_2

def test_compare_points_neq():
    point_1 = Point(0, 0)
    point_2 = Point(1, 0)

    assert point_1 != point_2

def test_compare_point_with_non_point():
    point = Point(0, 0)
    other = 0

    assert point != other

def test_compare_non_point_with_point():
    other = 0
    point = Point(0, 0)

    assert other != point

""" clone a Point """

def test_copy_point():
    point_1 = Point(1, 2)
    point_2 = copy(point_1)

    assert point_1 == point_2

""" check whether a Point lies on a given Line """

def test_point_on_line():
    point = Point(1, 2)
    line = Line(-2, 1, 0)

    actual = point.isOn(line)

    assert actual == True

def test_point_not_on_line():
    point = Point(1, 2)
    line = Line(2, 1, 0)

    actual = point.isOn(line)

    assert actual == False

def test_point_on_horizontal_line():
    point = Point(1, 1)
    line = Line(0, 1, -1)

    actual = point.isOn(line)

    assert actual == True

def test_point_not_on_horizontal_line():
    point = Point(1, 2)
    line = Line(0, 1, -1)

    actual = point.isOn(line)

    assert actual == False

def test_point_on_vertical_line():
    point = Point(1, 1)
    line = Line(1, 0, -1)

    actual = point.isOn(line)

    assert actual == True

def test_point_not_on_vertical_line():
    point = Point(2, 1)
    line = Line(1, 0, -1)

    actual = point.isOn(line)

    assert actual == False
