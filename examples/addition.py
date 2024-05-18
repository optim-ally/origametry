from origametry import Point, fold, reflect, distance


def origami_add(a, b):

    """ algorightm to add two *positive* numbers """

    # setup
    a1 = Point.Point(0, 0)
    a2 = Point.Point(0, a)

    b1 = Point.Point(1, 0)
    b2 = Point.Point(1, b)

    # connect end-to-end
    crease_1 = fold.fold(a1, b2)

    # mark reflected points
    c1 = reflect(a1, crease_1)  # should be equal to b1
    c2 = reflect(a2, crease_1)

    # get line through `b` points
    line_b = fold.fold(b1, b1, b2, b2)

    # fold line `c` onto line `b`
    # can shortcut using axiom 5: c2 onto line_b and through c1
    crease_2, crease_3 = fold.fold(c2, line_b, c1, c1)

    # mark reflected points
    d2 = reflect(c2, crease_2)
    e2 = reflect(c2, crease_3)

    # one of d, e is addition and the other is subtraction
    return max(
        distance(b1, d2),
        distance(b1, e2)
    )
