#!/usr/bin/env python
"""
Stub-files for scipy.signal. This module contains the type-annotations for
scipy's library for fourier-transformations and signal analysis.
"""
from typing import Tuple, Optional, Union, overload

from scientific_plots.types_ import Vector


def welch(
    Y: Union[Vector, list[float]],
    fs: Optional[float] = None,
    scaling: str = "density",
    window: Optional[str] = "hamming",
    nperseg: int = 10,
    detrend: bool = False) -> Tuple[Vector, Vector]: ...


def periodogram(
    Y: Union[Vector, list[float]],
    fs: Optional[float] = None,
    scaling: str = "density",
    window: Optional[str] = "hamming",
    detrend: bool = False) -> Tuple[Vector, Vector]: ...


Single = Union[Vector, list[float]]
Double = Union[tuple[Vector, Vector], tuple[list[float], list[float]]]


@overload
def savgol_filter(
    values: Single, window: Union[int, float], order: int,
    mode: str = "nearest") -> Vector: ...


@overload
def savgol_filter(
    values: Double, window: Union[int, float], order: int,
    mode: str = "nearest")\
        -> tuple[Vector, Vector]: ...


def sosfilt(
    sos: Single, x: Single, axis: int = -1, zi: Optional[Single] = None)\
        -> Vector: ...


def sosfiltfilt(
    sos: Single, x: Single, axis: int = -1, zi: Optional[Single] = None)\
        -> Vector: ...


def butter(
    N: int, Wn: Single, btype: str = "low", analog: bool = False,
    output: str = "ba", fs: Optional[float] = None) -> Vector: ...
