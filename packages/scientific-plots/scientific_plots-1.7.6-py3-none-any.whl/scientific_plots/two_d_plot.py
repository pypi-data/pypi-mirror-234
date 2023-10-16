#!/usr/bin/env python3
"""
This file contains the settings for 2D surface
plots
"""
from __future__ import annotations

from os.path import join
from math import pi
from queue import Queue
from threading import Thread
from subprocess import check_output
from typing import (
    List, Tuple, TypeVar, Union, Iterable, Any, Optional)
from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from numpy import array

from .plot_settings import apply_styles, rwth_gradient_map
from .types_ import Vector

mpl.use("Agg")
SURFACEFOLDER = join("simulation", "surface_data")

In = TypeVar("In", List[float], Tuple[float],
             Vector)


@apply_styles
def create_two_d_scatter_plot(
        X: In, Y: In, Z: In,
        folder: Union[str, Path],
        plot_title: str,
        xlabel: Optional[str], ylabel: Optional[str], zlabel: str)\
        -> None:
    """create two_d_plots"""
    # rearrange x, y, z to fit the shape needed for the plot
    fig = plt.figure()
    plt.set_cmap("jet")

    ax = fig.add_subplot(projection="3d")
    ax.scatter(Y, X, Z, cmap=rwth_gradient_map)

    if xlabel:
        ax.set_ylabel(xlabel)
    if ylabel:
        ax.set_xlabel(ylabel)
    ax.set_zlabel(zlabel)

    plt.tight_layout()

    plt.savefig(join(folder, plot_title.replace(" ", "_") + ".pdf"))


@apply_styles
def create_two_d_surface_plot(
        X: In, Y: In, Z: In,
        folder: Union[str, Path],
        plot_title: str,
        xlabel: Optional[str], ylabel: Optional[str], zlabel: str)\
        -> None:
    """create two_d_plots"""
    # rearrange x, y, z to fit the shape needed for the plot
    fig = plt.figure()
    plt.set_cmap("jet")
    Z_flat: Vector = array(Z)

    # X_two_d, Y_two_d=meshgrid(X_flat, Y_flat)

    ax = fig.add_subplot(projection="3d")
    # ax.plot_surface(X_two_d, Y_two_d, Z_flat, cmap=rwth_gradient_map)
    ax.plot_trisurf(Y, X, Z, cmap=rwth_gradient_map)

    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.set_zlabel(zlabel)

    ax.set_zlim(min(Z_flat) * 0.98, max(Z_flat) * 1.05)
    ax.set_xlim(min(Y), max(Y))
    ax.set_ylim(min(X), max(X))

    plt.tight_layout()

    plt.savefig(join(folder, plot_title.replace(" ", "_") + ".pdf"))


def get_leakage(data: Iterable[Any], var: str = "density",
                surface_file: Optional[str] = None) -> list[float]:
    """calculate the leakage for a given set of data
    @param data enumerable set of valve-objects
        which allow the determination of the leakage
    @return list of the same dimension for the leakage"""
    if surface_file is None:
        surface_path = join(SURFACEFOLDER, "c_q.dat")
    leakage_bin = join(".", "subroutines", "bin", "test_leakage")
    Y: list[float] = []
    X: list[float] = []
    q: Queue[Any] = Queue()
    # run every call of the fortran-code in parallel
    for d in data:  # put the data into the
        # queue to access them later as needed
        q.put(d)

    def work_of_queue() -> None:
        nonlocal X
        nonlocal Y
        while True:
            d = q.get()
            if d is None:
                return  # last data-point
            pressure = max(d.short.p)
            print(pressure)
            print(d.angle, d.wobble)
            C = float(check_output([leakage_bin, "-i", surface_path, "-P",
                                    f"{pressure}"]))
            # A=d.short.unroundness2
            A = d.short.sigma
            R = d.valve.seat.radius
            delta_p = d.dictionary["fluid-pressure"]["value"]
            Y += [delta_p * 2.0 * pi * R / A * C]
            X += [getattr(d, var)]

    threads = [Thread(target=work_of_queue) for i in range(16)]
    for thread in threads:  # start all threads
        thread.start()
        q.put(None)
    for thread in threads:  # wait for all threads to finish
        thread.join()
    return Y


def plot_2d_surface(
    data: Iterable[Any],
    folder: str = "simulation",
    var1: str = "angle",
    var2: str = "wobble",
    xlabel1: Optional[str] = None,
    xlabel2: Optional[str] = None,
    surface_file: Optional[str] = None,
) -> None:
    """create the two d surface plots of two given variables"""
    X = [getattr(d, var1) for d in data]
    Y = [getattr(d, var2) for d in data]
    pressure = [max(d.short.p) for d in data]
    A = [d.short.unroundness for d in data]
    leakage = get_leakage(data, surface_file=surface_file)

    create_two_d_scatter_plot(
        X, Y, pressure, folder, "two d pressure",
        xlabel1, xlabel2, "maximal pressure [MPa]"
    )
    create_two_d_scatter_plot(
        X, Y, A, folder, "two d area", xlabel1, xlabel2, "contact area [mm]"
    )
    create_two_d_scatter_plot(
        X, Y, leakage, folder,
        "two d leakage", xlabel2, xlabel2, "leakage [ml/s]"
    )
    create_two_d_surface_plot(
        X,
        Y,
        pressure,
        folder,
        "two d pressure surface",
        xlabel1,
        xlabel2,
        "maximal pressure [MPa]",
    )
    create_two_d_surface_plot(
        X, Y, A, folder, "two d area surface",
        xlabel1, xlabel2, "contact area [mm]"
    )
    create_two_d_surface_plot(
        X,
        Y,
        pressure,
        folder,
        "two d pressure surface",
        xlabel1,
        xlabel2,
        "maximal pressure [MPa]",
    )
    create_two_d_surface_plot(
        X, Y, leakage, folder, "two d leakage surface",
        xlabel2, xlabel2, "leakage [ml/s]"
    )
