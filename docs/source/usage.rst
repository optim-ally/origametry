Usage
=====

.. _points:
.. _lines:
.. _simulating_folds:

Points
------

**Origametry** provides a :code:`Point` class, which is a light wrapper around a pair of Cartesian coordinates.

.. code-block:: python

   from origametry import Point

   point = Point(3, 5)

   point.x
   # 3
   point.y
   # 5

It provides fuzzy equality checks against other points using the `math.isclose <https://docs.python.org/3/library/math.html#math.isclose>`_ function

.. code-block:: python

   p1 = Point(0, .1 + .2)
   p2 = Point(0, .3)

   p1 == p2
   # True

and an :code:`isOn` method for checking colinearity.

.. code-block:: python

   from origametry import Line

   point = Point(2, 5)
   line = Line(3, -1, 2)

   point.isOn(line)
   # True

Lines
-----

There is also a :code:`Line` class that stores a straight line in terms of the standard-form line equation :code:`ax + by + c = 0`, although it can be instantiated in several ways:

* with coefficients :code:`a`, :code:`b` and :code:`c` directly

.. code-block:: python

   from origametry import Line

   line = Line(3, -1, 2)

   line.a
   # 3
   line.b
   # -1
   line.c
   # 2

   # `c` can be omitted and defaults to 0
   line = Line(3, -1)

* with two distinct points

.. code-block:: python

   p1 = Point(3, 5)
   p2 = Point(8, 13)

   line = Line(p1, p2)

* with one point and a gradient

.. code-block:: python

   point = Point(2.5, 0)

   line = Line(point, .75)

* with just a gradient, which gives a line through the origin

.. code-block:: python

   # the line y = 0 (horizontal through the origin)
   line = Line(0)

   # the line y = x
   line = Line(1)

   # vertical line
   line = Line(math.inf)

* as the result of a :ref:`fold<Simulating folds>`.

Simulating folds
----------------

.. code-block:: python

    from origametry import point, fold

    # create two points on the plane
    p1 = Point(0, 1)
    p2 = Point(3, 5)

    # find the fold that puts `p1` onto `p2`
    crease = fold(p1, p2)
