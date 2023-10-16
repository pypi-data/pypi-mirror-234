#!/usr/bin/env python
"""
Stub-file for scipy.optimize. It contains only the typing-annotation for this
module.
"""

from typing import Tuple, Callable, List, Optional, TypeVar, Union, Any

from scientific_plots.types_ import Matrix, Vector, Tensor

Input = TypeVar("Input", float, list[float], Matrix, Vector, Tensor)


def curve_fit(
    func: Callable[..., Input],
    x: Union[Vector, list[float]],
    y: Union[Vector, list[float]],
    p0: Optional[Union[List[float], tuple[float]]] = None,
    bounds: Optional[Any] = None)\
    -> Tuple[Vector, Matrix]: ...


def brentq(
    func: Callable[[Input], Input],
    start: float,
    end: float,
    maxiter: int = 1000,
    xtol: Optional[float] = None,
    rtol: Optional[float] = None) -> float: ...


class OptimizeResult:
    """The class contains the result of the root-finding algorithm."""
    x: Vector
    success: bool
    status: int
    message: str


def root(
    func: Callable[[Input], Input],
    start: float) -> OptimizeResult: ...
