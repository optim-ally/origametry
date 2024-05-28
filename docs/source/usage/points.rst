.. _points:

Points
======

The :code:`Point` class is a light wrapper around a pair of Cartesian coordinates.

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
