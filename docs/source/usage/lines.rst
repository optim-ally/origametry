.. _lines:

Lines
=====

The :code:`Line` class stores a straight line in terms of the standard-form line equation :code:`ax + by + c = 0`, although it can be instantiated in several ways:

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

* with two distinct :ref:`points <points>`

.. code-block:: python

   p1 = Point(3, 5)
   p2 = Point(8, 13)

   line = Line(p1, p2)

* with one :ref:`point <points>` and a gradient

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

* as the result of a :ref:`fold <folding>`.

Like :ref:`points <points>`, lines have fuzzy equality checking that allows for small floating-point errors.

.. code-block:: python

   line_1 = Line(1, 0, .1 + .2)
   line_2 = Line(1, 0, .3)

   line_1 == line_2
   # True

A :code:`Line` object has properties :code:`a`, :code:`b` and :code:`c` for the coefficients of the equation :code:`ax + by + c = 0` that describes it.
It also has a :code:`gradient` property that is calculated from these coefficients.

.. code-block:: python

   line = Line(1, 2, 3)

   line.gradient
   # -0.5

Finally, it has an :code:`intersection` method to find the point at which it crosses another line.

.. code-block:: python

   line_1 = Line(1, -1, 0)
   line_2 = Line(0, 1, -2)

   line_1.intersection(line_2)
   # Point(2, 2)

For parallel lines there is no intersection, so the method returns :code:`None`.

.. code-block:: python

   line_1 = Line(1, -1, 0)
   line_2 = Line(1, -1, 5)

   line_1.intersection(line_2)
   # None
