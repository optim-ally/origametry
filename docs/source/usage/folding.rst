.. _folding:

Folding
=======

A "fold" is a reflection of points and/or lines across a crease. Origametry exports two functions for working with folds: :code:`fold` and :code:`reflect`.

The :code:`reflect` function simply returns the reflection of a point or line across a given crease:

.. code-block:: python

    from origametry import reflect

    # get the reflection of `point_1` when folded across the crease
    point_2 = reflect(point_1, crease)

    # you can also reflect lines
    line_2 = reflect(line_1, crease)

The :code:`fold` function is much more complex. It takes a pairwise series of points and/or lines and tries to find a fold that reflects every element onto its pair. The function returns the crease of that fold or a list of creases, or :code:`None` if no such fold is possible. This concept is best explained with pictures.

Fold :code:`p1` onto :code:`p2` (:ref:`axiom 2 <axioms>`):

.. image:: ../../images/axiom_2.png
    :width: 360
    :alt: Diagram of a fold placing a point onto a point

.. code-block:: python

    from origametry import point, fold

    # create two points on the plane
    p1 = Point(0, 1)
    p2 = Point(3, 5)

    # find the fold that puts `p1` onto `p2`
    crease = fold(p1, p2)

Fold :code:`line_1` onto :code:`line_2` (:ref:`axiom 3 <axioms>`):

.. image:: ../../images/axiom_3.png
    :width: 360
    :alt: Diagram of a fold placing a line onto a parallel line

.. code-block:: python

    crease = fold(line_1, line_2)

If :code:`line_1` and :code:`line_2` are not parallel, there are 2 folds that work:

.. image:: ../../images/axiom_3_double.png
    :width: 360
    :alt: Diagram of a fold placing a line onto a line

.. code-block:: python

    creases = fold(line_1, line_2)

    crease_1 = creases[0]
    crease_2 = creases[1]

Fold :code:`p1` onto :code:`line_1` **AND** :code:`p2` onto :code:`line_2` (:ref:`axiom 6 <axioms>`):

.. image:: ../../images/axiom_6.png
    :width: 360
    :alt: Diagram of a fold placing a point onto a line and a second point onto another line

.. code-block:: python

    creases = fold(p1, line_1, p2, line_2)

    crease_1 = creases[0]
    crease_2 = creases[1]
    crease_3 = creases[2]

And here's an example of :ref:`axiom 6 <axioms>` with no solutions:

.. image:: ../../images/axiom_6_none.png
    :width: 360
    :alt: Diagram showing a lack of folds placing a point onto a line and another point onto a parallel line

.. code-block:: python

    creases = fold(p1, line_1, p2, line_2)

    assert creases is None

Some :ref:`axioms` require that a crease passes through a point. This is equivalent to reflecting that point onto itself.

Thus we can fold through :code:`p1` and :code:`p2` (:ref:`axiom 1 <axioms>`):

.. image:: ../../images/axiom_1.png
    :width: 360
    :alt: Diagram of a fold through two points

.. code-block:: python

    crease = fold(p1, p1, p2, p2)

And fold :code:`p1` onto :code:`line_1` through :code:`p2` (:ref:`axiom 5 <axioms>`):

.. image:: ../../images/axiom_5.png
    :width: 360
    :alt: Diagram of a fold through a point that places another point onto a line

.. code-block:: python

    creases = fold(p1, line_1, p2, p2)

    crease_1 = creases[0]
    crease_2 = creases[1]

Finally, some :ref:`axioms` require that a crease is perpendicular to a line. This is nearly equivelent to reflecting a line onto itself, with the caveat that a crease going along a line also reflects it onto iself. Since the second case is trivial - the crease is identical to the original line - we choose to always interpret :code:`fold(L, L, ...)` as being perpendicular to the line :code:`L`.

Fold through :code:`p1` perpendicular to :code:`line_1` (:ref:`axiom 4 <axioms>`):

.. image:: ../../images/axiom_4.png
    :width: 360
    :alt: Diagram of a fold through a point and perpendicular to a line

.. code-block:: python

    crease = fold(p1, p1, line_1, line_1)

Fold :code:`p1` onto :code:`line_1` perpendicular to :code:`line_2` (:ref:`axiom 7 <axioms>`):

.. image:: ../../images/axiom_7.png
    :width: 360
    :alt: Diagram of a fold perpendicular to a line that places a point onto a line

.. code-block:: python

    crease = fold(p1, line_1, line_2, line_2)

An example of :ref:`axiom 7 <axioms>` with no solutions (:code:`line_1` and :code:`line_2` are parallel):

.. image:: ../../images/axiom_7_none.png
    :width: 360
    :alt: Diagram showing an absence of fold perpendicular to a line that place a point onto a parallel line

.. code-block:: python

    creases = fold(p1, line_1, line_2, line_2)

    assert creases is None
