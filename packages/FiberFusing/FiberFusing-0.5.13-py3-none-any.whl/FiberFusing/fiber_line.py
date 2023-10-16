#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Built-in imports
import numpy
from dataclasses import dataclass

# Local imports
from FiberFusing.buffer import Circle, Point
from FiberFusing.connection_base import ConnectionOptimization
from FiberFusing import utils

# Other imports
from MPSPlots.Render2D import SceneList, Axis


@dataclass
class FiberLine():
    number_of_fibers: int
    """ Number of fiber in the ring """
    fiber_radius: float
    """ Radius of the radius of the rings, same for every ringe here """

    def __post_init__(self):
        pass

    def plot(self) -> Scene2D:
        """
        Plot the structure.

        :returns:   Scene
        :rtype:     Scene2D
        """
        figure = SceneList(unit_size=(6, 6))

        ax = figure.append_ax(
            x_label=r'x',
            y_label=r'y',
            show_grid=True,
            equal_limits=True,
            equal=True
        )


        return figure