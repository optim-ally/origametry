# Origametry

Python package to perform calculations using the Huzita-Justin axioms for 2-dimensional origami

## The Axioms

Discovered by French mathematician Jacques Justin in 1986 and rediscovered by Humiaki Huzita and Koshiro Hatori, these 7 axioms can construct every possible single-fold alignment in the plane.

1. Given two distinct points P1 and P2, there is a unique fold that passes through both of them.
2. Given two distinct points P1 and P2, there is a unique fold that places P1 onto P2.
3. Given two distinct lines L1 and L2, there is a fold that places L1 onto L2.
4. Given a point P1 and a line L1, there is a unique fold perpendicular to L1 that passes through point P1.
5. Given two points P1 and P2 and a line L1, there is a fold that places P1 onto L1 and passes through P2.
6. Given two points P1 and P2 and two lines L1 and L2, there is a fold that places P1 onto L1 and P2 onto L2.
7. Given one point P and two lines L1 and L2, there is a fold that places P onto L1 and is perpendicular to L2.

Axiom 3 may have 1 or 2 solutions.
Axiom 5 may have 0, 1, or 2 _non-trivial_ solutions.
Axiom 6 may have 0, 1, 2, or 3 _non-trivial_ solutions.
Axiom 7 may have 0 or 1 _non-trivial_ solutions.

Note that axioms 5, 6 and 7 have infinitely many trivial solutions if any of the points **already** lie on their required lines.

## Installation

```
pip install origametry
```

## Usage

From only a few starting points, you can generate complex sequences of folds

```py
from origametry import Point, fold, show

point_1 = Point(0, 0)
point_2 = Point(2, 1)

# axiom 2: point onto point
line = fold(point_1, point_2)

# axiom 5: point onto line through another point (2 solutions)
lines = fold(point_1, line, point_2, point_2)
```

~~And view your resulting crease pattern~~ (TODO)

```py
show(point_1, point_2, line, lines)
```

#### Points

A "point" is a simple container object for 2-dimensional Cartesian coordinates.

```py
point = Point(3, 5)

point.x
# 3
point.y
# 5
```

#### Lines

A straight line (or "crease") in the plane can be created in several ways:

- two distinct points

```py
point_1 = Point(3, 5)
point_2 = Point(8, 13)

line = Line(point_1, point_2)
```

- coefficients of standard-form equation `ax + by + c = 0`

```py
line = Line(1, 3, -2)

# `c` defaults to 0
line = Line(1, 3)
```

- point and gradient

```py
point = Point(2.5, 0)

line = Line(point, .75)
```

- gradient through origin

```py
# the line y = 0 (horizontal through the origin)
line = Line(0)

# the line y = x
line = Line(1)

# vertical line
line = Line(math.inf)
```

- as the result of [a fold](#folds)

##### intersection

A point can also be created at the intersection of two lines. This method returns `None` is the lines are parallel (i.e. they do not intersect).

```py
point = line_1.intersection(line_2)
```

#### Folds

A "fold" is a reflection of points and/or lines across a crease. Origametry exports two functions for working with folds: `fold` and `reflect`.

The `reflect` function simply returns the reflection of a point or line across a given crease:

```py
point_2 = reflect(point_1, crease)

line_2 = reflect(line_1, crease)
```

The `fold` function is much more complex. It takes a pairwise series of points and/or lines and tries to find a fold that reflects every element onto its pair. The function returns the crease of that fold or a list of creases, or `None` if no such fold is possible. This concept is best explained with pictures.

Fold `P1` onto `P2` (axiom 2):

<img src="https://github.com/optim-ally/origametry/assets/23644615/f21b61ba-96bc-45e9-8c69-95de22871ef3" width="360">

```py
L = fold(P1, P2)
```

Fold `L1` onto `L2` (axiom 3):

<img src="https://github.com/optim-ally/origametry/assets/23644615/c677a61b-296b-4949-9e97-5412d22dbffa" width="360">

```py
L3 = fold(L1, L2)
```

If `L1` and `L2` are not parallel, there are 2 folds that work:

<img src="https://github.com/optim-ally/origametry/assets/23644615/b2261d10-4037-42ac-86b0-9b4ef0a016fa" width="360">

```py
creases = fold(L1, L2)

L3 = creases[0]
L4 = creases[1]
```

Fold `P1` onto `L1` **AND** `P2` onto `L2` (axiom 6):

<img src="https://github.com/optim-ally/origametry/assets/23644615/0455501c-c76c-435b-b3fa-d130dd465991" width="360">

```py
creases = fold(P1, L1, P2, L2)

L3 = creases[0]
L4 = creases[1]
L5 = creases[2]
```

And here's an example of axiom 6 with no solutions:

<img src="https://github.com/optim-ally/origametry/assets/23644615/bb3ca3ce-cf30-4369-8da5-1a72743e758f" width="360">

```py
creases = fold(P1, L1, P2, L2)

assert creases is None
```

Some axioms require that a crease passes through a point. This is equivalent to reflecting that point onto itself.

Thus we can fold through `P1` and `P2` (axiom 1):

<img src="https://github.com/optim-ally/origametry/assets/23644615/71e2f4f6-00ea-4183-a587-d62dcc4f39b0" width="360">

```py
L = fold(P1, P1, P2, P2)
```

And fold `P1` onto `L1` through `P2` (axiom 5):

<img src="https://github.com/optim-ally/origametry/assets/23644615/9ee7b88a-d7ff-4bdf-b8eb-3a0ee5227cdf" width="360">

```py
creases = fold(P1, L1, P2, P2)

L2 = creases[0]
L3 = creases[1]
```

Finally, some axioms require that a crease is perpendicular to a line. This is nearly equivelent to reflecting a line onto itself, with the caveat that a crease going along a line also reflects it onto iself. Since the second case is trivial - the crease is identical to the original line - we choose to always interpret `fold(L, L, ...)` as being perpendicular to the line `L`.

Fold through `P1` perpendicular to `L1` (axiom 4):

<img src="https://github.com/optim-ally/origametry/assets/23644615/ebe8feba-8c59-4dda-95c3-bf74af2600a0" width="360">

```py
L2 = fold(P1, P1, L1, L1)
```

Fold `P1` onto `L1` perpendicular to `L2` (axiom 7):

<img src="https://github.com/optim-ally/origametry/assets/23644615/1f9b7bc4-9822-4b16-8835-6b56ce237776" width="360">

```py
L3 = fold(P1, L1, L2, L2)
```

An example of axiom 7 with no solutions (`L1` and `L2` are parallel):

<img src="https://github.com/optim-ally/origametry/assets/23644615/6677ffc0-d280-43d9-92c3-d79afb66a682" width="360">

```py
creases = fold(P1, L1, L2, L2)

assert creases is None
```
