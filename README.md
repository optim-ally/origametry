# Origametry

Python package to perform calculations using the Huzita-Justin axioms for 2-dimensional origami

- **Documentation:** https://origametry.readthedocs.io

## Installation

```
pip install origametry
```

## Getting Started

From only a few starting points, you can generate complex sequences of folds

```py
from origametry import Point, fold, show

point_1 = Point(0, 0)
point_2 = Point(2, 1)

# axiom 2: point onto point
line = fold(point_1, point_2)

# axiom 5: point onto line through another point (2 solutions)
creases = fold(point_1, line, point_2, point_2)
```

And view your resulting crease pattern

```py
show(point_1, point_2, line, creases=creases)
```

![example plot](https://github.com/optim-ally/origametry/raw/main/example_plot.png)
