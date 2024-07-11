Origametry Documentation
========================

**Origametry** is a Python library for simulating fold sequences based on the Huzita-Hatori-Justin axioms of origami.

Discovered by French mathematician Jacques Justin in 1986 and rediscovered by Humiaki Huzita and Koshiro Hatori, these 7 axioms can construct every possible single-fold alignment in the plane.

.. _axioms:

1. Given two distinct points P1 and P2, there is a unique fold that passes through both of them.
2. Given two distinct points P1 and P2, there is a unique fold that places P1 onto P2.
3. Given two distinct lines L1 and L2, there is a fold that places L1 onto L2.
4. Given a point P1 and a line L1, there is a unique fold perpendicular to L1 that passes through point P1.
5. Given two points P1 and P2 and a line L1, there is a fold that places P1 onto L1 and passes through P2.
6. Given two points P1 and P2 and two lines L1 and L2, there is a fold that places P1 onto L1 and P2 onto L2.
7. Given one point P and two lines L1 and L2, there is a fold that places P onto L1 and is perpendicular to L2.

Contents
--------

.. toctree::

   installation
   usage/index

What's in the name?
-------------------

The name **Origametry** is a `portmanteau <https://en.wikipedia.org/wiki/Blend_word>`_ of "origami" - the ancient Japanese art of paper folding - and "geometry" - the mathematical study of points, lines and surfaces (among other things).

It has been used to describe the field of computational origami for several years, and may have been first used by Thomas Hull in his `book <https://www.cambridge.org/us/universitypress/subjects/mathematics/recreational-mathematics/origametry-mathematical-methods-paper-folding>`_ of the same name.
