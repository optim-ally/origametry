from src.line import Line
from src.point import Point
from src.reflect import reflect


""" reflect a point """

def test_reflect_point():
    point = Point(0, 0)
    crease = Line(1, 1, -1)

    reflection = reflect(point, crease)

    assert reflection == Point(1, 1)

def test_reflect_point_horizontally():
    point = Point(0, 0)
    crease = Line(1, 0, -1)

    reflection = reflect(point, crease)

    assert reflection == Point(2, 0)

def test_reflect_point_vertically():
    point = Point(0, 0)
    crease = Line(0, 1, -1)

    reflection = reflect(point, crease)

    assert reflection == Point(0, 2)

def test_reflect_point_across_origin():
    point = Point(0, 1)
    crease = Line(0, 1, 0)

    reflection = reflect(point, crease)

    assert reflection == Point(0, -1)

""" reflect a line """

def test_reflect_line():
    line = Line(1, 2)
    crease = Line(1, 1, -1)

    reflection = reflect(line, crease)

    assert reflection == Line(-2 / 3, -1 / 3, 1)

def test_reflect_line_horizontally():
    line = Line(1, 2)
    crease = Line(1, 0, -1)

    reflection = reflect(line, crease)

    assert reflection == Line(-.5, 1, 1)

def test_reflect_line_vertically():
    line = Line(1, 2)
    crease = Line(0, 1, -1)

    reflection = reflect(line, crease)

    assert reflection == Line(.25, -.5, 1)

def test_reflect_line_across_origin():
    line = Line(1, 2)
    crease = Line(0, 1, 0)

    reflection = reflect(line, crease)

    assert reflection == Line(-.5, 1, 0)

def test_reflect_vertical_line():
    line = Line(1, 0, -1)
    crease = Line(1, 1, -1)

    reflection = reflect(line, crease)

    assert reflection == Line(0, 1)

def test_reflect_vertical_line_horizontally():
    line = Line(1, 0, -1)
    crease = Line(1, 0, -2)

    reflection = reflect(line, crease)

    assert reflection == Line(1, 0, -3)

def test_reflect_vertical_line_vertically():
    line = Line(1, 0, -1)
    crease = Line(0, 1, -1)

    reflection = reflect(line, crease)

    assert reflection == line

def test_reflect_vertical_line_across_origin():
    line = Line(1, 0, -1)
    crease = Line(1, 0, 0)

    reflection = reflect(line, crease)

    assert reflection == Line(1, 0, 1)

def test_reflect_horizontal_line():
    line = Line(0, 1, -1)
    crease = Line(1, 1, -1)

    reflection = reflect(line, crease)

    assert reflection == Line(1, 0)

def test_reflect_horizontal_line_horizontally():
    line = Line(0, 1, -1)
    crease = Line(1, 0, -2)

    reflection = reflect(line, crease)

    assert reflection == line

def test_reflect_horizontal_line_vertically():
    line = Line(0, 1, -1)
    crease = Line(0, 1, -2)

    reflection = reflect(line, crease)

    assert reflection == Line(0, 1, -3)

def test_reflect_horizontal_line_across_origin():
    line = Line(0, 1, -1)
    crease = Line(0, 1, 0)

    reflection = reflect(line, crease)

    assert reflection == Line(0, 1, 1)
