import pytest
from unittest.mock import Mock, patch, call

from src.origametry.line import Line
from src.origametry.point import Point
from src.origametry.fold import fold
from src.origametry.show import show


""" fixtures """

@pytest.fixture
def mock_plot():
    with patch("matplotlib.pyplot.plot") as mockplot:
        yield mockplot


@pytest.fixture
def mock_axes():
    with patch("matplotlib.pyplot.gca") as mockgca:
        mockaxes = Mock()
        mockgca.return_value = mockaxes
        yield mockaxes


@pytest.fixture(autouse=True)
def mock_show():
    with patch("matplotlib.pyplot.show") as mockshow:
        yield mockshow


""" tests """

def test_show_plot(mock_show):
    show()

    mock_show.assert_called_once_with()


def test_set_equal_aspect_ratio(mock_axes):
    show()

    mock_axes.set_aspect.assert_called_once_with("equal", adjustable="box")


def test_single_point(mock_plot, mock_axes):
    point = Point(10, 13)

    show(point)

    mock_plot.assert_called_once_with(10, 13, "ok", markerfacecolor="#d0d")
    mock_axes.set_xlim.assert_called_once_with(9, 11)
    mock_axes.set_ylim.assert_called_once_with(12, 14)


def test_single_line(mock_plot, mock_axes):
    line = Line(1, -1, 2)

    show(line)

    mock_plot.assert_called_once_with([-1, 1], [1, 3], color="#d0d")
    mock_axes.set_xlim.assert_called_once_with(-1, 1)
    mock_axes.set_ylim.assert_called_once_with(1, 3)


def test_single_crease(mock_plot, mock_axes):
    crease = Line(1, 2, 1)

    show(creases=crease)

    mock_plot.assert_called_once_with([-1, 1], [0, -1], "--", color="#abf")
    mock_axes.set_xlim.assert_called_once_with(-1, 1)
    mock_axes.set_ylim.assert_called_once_with(-1.5, .5)


def test_single_crease_as_list(mock_plot, mock_axes):
    crease = Line(1, 0, 0)

    show(creases=[crease])

    mock_plot.assert_called_once_with([0, 0], [-1, 1], "--", color="#abf")
    mock_axes.set_xlim.assert_called_once_with(-1, 1)
    mock_axes.set_ylim.assert_called_once_with(-1, 1)


def test_none_as_creases(mock_plot, mock_axes):
    show(creases=None)

    mock_plot.assert_not_called()
    mock_axes.set_xlim.assert_called_once_with(-1, 1)
    mock_axes.set_ylim.assert_called_once_with(-1, 1)


def test_two_points(mock_plot, mock_axes):
    p1 = Point(1, 2)
    p2 = Point(8, 3)

    show(p1, p2)

    mock_plot.assert_has_calls([
        call(1, 2, "ok", markerfacecolor="#d0d"),
        call(8, 3, "ok", markerfacecolor="#d0d"),
    ])
    mock_axes.set_xlim.assert_called_once_with(-.75, 9.75)
    mock_axes.set_ylim.assert_called_once_with(-2.75, 7.75)


def test_point_and_line(mock_plot, mock_axes):
    point = Point(1, 2)
    line = Line(0, 1, -1)

    show(point, line)

    mock_plot.assert_has_calls([
        call(1, 2, "ok", markerfacecolor="#d0d"),
        call([.25, 1.75], [1, 1], color="#d0d"),
    ])
    mock_axes.set_xlim.assert_called_once_with(.25, 1.75)
    mock_axes.set_ylim.assert_called_once_with(.75, 2.25)


def test_point_and_crease(mock_plot, mock_axes):
    point = Point(1, 2)
    crease = Line(0, 1, -1)

    show(point, creases=[crease])

    mock_plot.assert_has_calls([
        call(1, 2, "ok", markerfacecolor="#d0d"),
        call([.25, 1.75], [1, 1], "--", color="#abf"),
    ])
    mock_axes.set_xlim.assert_called_once_with(.25, 1.75)
    mock_axes.set_ylim.assert_called_once_with(.75, 2.25)


def test_two_lines(mock_plot, mock_axes):
    line_1 = Line(1, 1, 0)
    line_2 = Line(0, 1, -1)

    show(line_1, line_2)

    mock_plot.assert_has_calls([
        call([-2, 0], [2, 0], color="#d0d"),
        call([-2, 0], [1, 1], color="#d0d"),
    ])
    mock_axes.set_xlim.assert_called_once_with(-2, 0)
    mock_axes.set_ylim.assert_called_once_with(0, 2)


def test_line_and_crease(mock_plot, mock_axes):
    line = Line(1, 1, 0)
    crease = Line(0, 1, -1)

    show(line, creases=crease)

    mock_plot.assert_has_calls([
        call([-2, 0], [2, 0], color="#d0d"),
        call([-2, 0], [1, 1], "--", color="#abf"),
    ])
    mock_axes.set_xlim.assert_called_once_with(-2, 0)
    mock_axes.set_ylim.assert_called_once_with(0, 2)


def test_two_creases(mock_plot, mock_axes):
    crease_1 = Line(1, 1, 0)
    crease_2 = Line(0, 1, -1)

    show(creases=[crease_1, crease_2])

    mock_plot.assert_has_calls([
        call([-2, 0], [2, 0], "--", color="#abf"),
        call([-2, 0], [1, 1], "--", color="#abf"),
    ])
    mock_axes.set_xlim.assert_called_once_with(-2, 0)
    mock_axes.set_ylim.assert_called_once_with(0, 2)


def test_parallel_lines_and_creases(mock_plot, mock_axes):
    line_1 = Line(0, 1, -1)
    line_2 = Line(0, 1, -3)
    crease = fold(line_1, line_2)

    show(line_1, line_2, creases=crease)

    mock_plot.assert_has_calls([
        call([-1.5, 1.5], [1, 1], color="#d0d"),
        call([-1.5, 1.5], [3, 3], color="#d0d"),
        call([-1.5, 1.5], [2, 2], "--", color="#abf"),
    ])
    mock_axes.set_xlim.assert_called_once_with(-1.5, 1.5)
    mock_axes.set_ylim.assert_called_once_with(.5, 3.5)


def test_custom_bounding_box(mock_axes):
    point = Point(0, 0)

    show(point, bounding_box=(-80, -10, 20, 10))

    mock_axes.set_xlim.assert_called_once_with(-80, 20)
    mock_axes.set_ylim.assert_called_once_with(-10, 10)


def test_line_outside_custom_bounding_box(mock_plot, mock_axes):
    line = Line(0, 1, -1)

    show(line, bounding_box=(-50, -50, 0, 0))

    mock_plot.assert_not_called()
    mock_axes.set_xlim.assert_called_once_with(-50, 0)
    mock_axes.set_ylim.assert_called_once_with(-50, 0)
