import pytest
from math import sqrt

from src.line import Line
from src.point import Point
from src.helpers import distance


""" distance """

def test_distance_point_to_point():
    point_1 = Point(0, 0)
    point_2 = Point(3, 4)

    assert distance(point_1, point_2) == 5

def test_distance_point_to_line():
    point = Point(0, 0)
    line = Line(1, -1, 2)

    assert distance(point, line) == sqrt(2)

def test_distance_line_to_point():
    line = Line(1, -1, 2)
    point = Point(0, 0)

    assert distance(line, point) == sqrt(2)

def test_distance_line_to_line():
    line_1 = Line(1, -1, 2)
    line_2 = Line(1, -1, 2)

    with pytest.raises(TypeError):
        distance(line_1, line_2)
