import matplotlib.pyplot as plt
from typing import Union, Optional

from .line import Line
from .point import Point
from .helpers import projection, points_on_line, remove_duplicates


def _find_bounding_box(points: list[Point], lines: list[Line]):
    if points == [] and lines == []:
        # default empty box
        return (-1, -1, 1, 1)

    # build a list of "points of interest"
    intersections: list[Point] = []
    projections: list[Point] = []

    if lines is not None:
        # include any intersections of lines
        for i, line_a in enumerate(lines):
            for line_b in lines[i + 1:]:
                if intersection := line_a.intersection(line_b):
                    intersections.append(intersection)

        # include at least one point on every line (so some part of each line is shown)
        if points is not None:
            for point in points:
                for line in lines:
                    projections.append(projection(point, line))

    points_of_interest = remove_duplicates(list(points) + intersections + projections)

    if len(points_of_interest) == 0:
        # only one line or parallel lines
        random_point = next(points_on_line(lines[0], 1))

        points_of_interest.append(random_point)
        points_of_interest += [projection(random_point, line) for line in lines[1:]]

    # get a box containing all points of interest
    min_x = min(point.x for point in points_of_interest)
    min_y = min(point.y for point in points_of_interest)
    max_x = max(point.x for point in points_of_interest)
    max_y = max(point.y for point in points_of_interest)

    # extend the bounding box by a small, non-zero margin
    margin = max(max_x - min_x, max_y - min_y) / 4
    if margin == 0:
        margin = 1

    min_x -= margin
    min_y -= margin
    max_x += margin
    max_y += margin

    # standardise the aspect ratio
    desired_ratio = 1
    actual_ratio = (max_y - min_y) / (max_x - min_x)

    if actual_ratio < desired_ratio:
        dy = (desired_ratio - actual_ratio) * (max_x - min_x)
        min_y -= dy / 2
        max_y += dy / 2
    elif actual_ratio > desired_ratio:
        dx = (1 / desired_ratio - 1 / actual_ratio) * (max_y - min_y)
        min_x -= dx / 2
        max_x += dx / 2

    return min_x, min_y, max_x, max_y


def _trim_to_box(
    line: Line, min_x: float, min_y: float, max_x: float, max_y: float
) -> Optional[tuple[Point, Point]]:
    # find points of intersection (if they exist) with each bounding line
    cross_min_x = line.intersection(Line(1, 0, -min_x))
    cross_min_y = line.intersection(Line(0, 1, -min_y))
    cross_max_x = line.intersection(Line(1, 0, -max_x))
    cross_max_y = line.intersection(Line(0, 1, -max_y))

    # at least two of these will be on the edge of the box,
    # while others may be outsde the box, None, or duplicates
    within_box: list[Point] = []

    for point in (cross_min_x, cross_max_x):
        if point and min_y <= point.y <= max_y:
            within_box.append(point)
    for point in (cross_min_y, cross_max_y):
        if point and min_x <= point.x <= max_x:
            within_box.append(point)

    within_box = remove_duplicates(within_box)

    if len(within_box) < 2:
        return None
    if len(within_box) == 2:
        return tuple(within_box)
    if len(within_box) > 2:  # pragma: no cover
        # this can happen due to floating point errors at the corners of the box
        if cross_min_x in within_box and cross_max_x in within_box:
            return (cross_min_x, cross_max_x)
        if cross_min_y in within_box and cross_max_y in within_box:
            return (cross_min_y, cross_max_y)


def show(
    *points_and_lines: list[Union[Point, Line]],
    creases: Optional[Union[list[Line], Line]]=None,
    bounding_box: Optional[tuple[Union[int, float]]]=None
):
    points = [x for x in points_and_lines if isinstance(x, Point)]
    lines = [x for x in points_and_lines if isinstance(x, Line)]
    if creases is None:
        creases = []
    elif isinstance(creases, Line):
        creases = [creases]
    else:
        creases = list(creases)
    box = bounding_box or _find_bounding_box(points, lines + creases)

    for point in points:
        plt.plot(point.x, point.y, "ok", markerfacecolor="#d0d")

    for line in lines:
        if (trimmed := _trim_to_box(line, *box)) is not None:
            start, end = trimmed
            plt.plot([start.x, end.x], [start.y, end.y], color="#d0d")

    for crease in creases:
        if (trimmed := _trim_to_box(crease, *box)) is not None:
            start, end = trimmed
            plt.plot([start.x, end.x], [start.y, end.y], "--", color="#abf")

    ax = plt.gca()
    ax.set_aspect("equal", adjustable="box")
    ax.set_xlim(box[0], box[2])
    ax.set_ylim(box[1], box[3])

    plt.show()
