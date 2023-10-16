#!/usr/bin/env python3
"""this module contains functions, which are useful for
analysing data """
from __future__ import annotations
from math import sqrt
from typing import Union, overload

from scipy.stats import linregress
import numpy as np

from .types_ import Vector, Matrix


ArrayLike = Union[list[float], Vector]
MatrixLike = Union[list[list[float]], Matrix]


@overload
def get_hrms(X: ArrayLike, Y: ArrayLike) -> float: ...


@overload
def get_hrms(X: ArrayLike, Y: MatrixLike) -> Vector: ...


def get_hrms(X: ArrayLike, Y: Union[ArrayLike, MatrixLike])\
        -> Union[float, Vector]:
    """calculate R_q or h_rms based on real space data
    calculate a single R_q if Y is a plain
    array and take the average if it is an array of arrays"""
    if isinstance(Y, list):
        Y = np.array(Y)
    if isinstance(X, list):
        X = np.array(X)
    if Y.ndim == 1:
        Y = np.array([Y])
    h_rms = []
    for y in Y:
        res = linregress(X, y)
        alpha = res[0]
        beta = res[0]
        y_lin = [y_i - alpha * x - beta for x, y_i in zip(X, y)]
        mean_y = sum(y_lin) / len(y_lin)
        y_lin = [y_i - mean_y for y_i in y_lin]
        h_rms += [sqrt(sum(y_lin_i ** 2 for y_lin_i in y_lin))]
    mean_h_rms = sum(h_rms) / len(h_rms)
    return mean_h_rms
