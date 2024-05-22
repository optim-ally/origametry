Usage
=====

.. _installation:

Installation
------------

Install Origametry using pip:

.. code-block:: console

   $ pip install origametry

Simulating Folds
----------------

.. code-block:: python

    from origametry import point, fold

    # create two points on the plane
    p1 = Point(0, 1)
    p2 = Point(3, 5)

    # find the fold that puts `p1` onto `p2`
    crease = fold(p1, p2)
