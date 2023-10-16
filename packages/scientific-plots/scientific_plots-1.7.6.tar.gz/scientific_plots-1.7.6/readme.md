# Scientific Plots
Create and save plots in scientific style

## Table of Contents
[[_TOC_]]

## Overview
This python module includes useful methods and definitions for various python
projects.
The focus lies of on the automatic creation of a set of plots, which are
designed to be used in scientific journals, dissertations and presentations.
The most important components are the definitions of types compatible
for numpy, located in `types_.py`, and the typing stubs in `stubs/`. These
typing stubs are also distributed in this package.

## Plotting
The easiest way to implement the plotting features provided by this library, is
to use one of the predefined function in `scientific_plots.default_plots`.
Alternatively, any plotting functions can be decorated by using the
`apply_styles` decorator in `scientific_plots.plot_settings`.

For example, this could look like this:
```
import matplotlib.pyplot as plt
from scientific_plots.plot_settings import apply_styles

@apply_styles
def plot_something() -> None:
    """Example function."""
    plt.plot(...)
    ...
    plt.savefig("subfolder/your_plot_name.pdf")
```

The script will create a bunch of plots and place them in the given location
next to your given path. Thus, it is advisable to create a different subfolder
for new plots.

For three-dimensional plots, it is recommended to set the optional argument
*three_d* of the decorator to true:
```
@apply_styles(three_d=True)
def plot_function():
    ...
```

Alternatively, this package provides default plot settings in the submodule
*default_plots*. The provided function apply a default design, which should
look good in most situations.

```
from scientific_plots.default_plots import plot

plot(x, y, "x_label", "y_label", "subfolder/filename.pdf")
```

## Types
Additional Vector like types for numpy-arrays are provided in
`scientifc_plots.types_`.  These types can be used for static type checking
using mypy.

## Typing Stubs
Addtional typing stubs for scipy, matplotlib and numba are provided and
installed by this package. These packages do not provide type hints on their
own.
