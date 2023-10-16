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
from MPSPlots.Render2D import SceneList


@dataclass
class FiberRing(ConnectionOptimization):
    number_of_fibers: int
    """ Number of fiber in the ring """
    fiber_radius: float
    """ Radius of the radius of the rings, same for every ringe here """
    angle_shift: float = 0
    """ Shift angle for the ring configuration """
    tolerance_factor: float = 1e-10

    def __post_init__(self):
        self.angle_list = numpy.linspace(0, 360, self.number_of_fibers, endpoint=False)
        self.angle_list += self.angle_shift
        self.delta_angle = (self.angle_list[1] - self.angle_list[0])

        centers = self.compute_centers(distance_from_center="not-fused")
        self.compute_fiber_list(centers=centers)

    def scale_position(self, factor: float) -> None:
        """
        Scale down the distance between each cores.

        :param      factor:  The scaling factor
        :type       factor:  float
        """
        for fiber in self.fiber_list:
            fiber.scale_position(factor=factor)

    def shift_position(self, shift: list) -> None:
        """
        Scale down the distance between each cores.

        :param      factor:  The scaling factor
        :type       factor:  float
        """
        for fiber in self.fiber_list:
            fiber.shift_position(shift=shift)

    def compute_fiber_list(self, centers) -> None:
        self.fiber_list = []

        for n, point in enumerate(centers):
            fiber_circle = Circle(
                radius=self.fiber_radius,
                position=point,
                name=f' Fiber {n}'
            )

            self.fiber_list.append(fiber_circle)

    def set_fusion_degree(self, fusion_degree: float) -> None:
        """
        Changing the fiber position according to the fusion degree
        as it is described the Suzanne Lacroix article.

        :param      fusion_degree:  Value describe the fusion degree of the structure the higher the value to more fused are the fibers [0, 1].
        :type       fusion_degree:  float
        """
        if fusion_degree == 0:
            distance_from_center = "not-fused"
        else:
            alpha = (2 - self.number_of_fibers) * numpy.pi / (2 * self.number_of_fibers)

            distance_from_center = (1 + numpy.cos(alpha)) - numpy.sqrt(self.number_of_fibers) * numpy.cos(alpha)

            distance_from_center = (self.fiber_radius - (distance_from_center * self.fiber_radius) * fusion_degree)

            distance_from_center *= 1 / (numpy.cos(alpha))

        centers = self.compute_centers(distance_from_center=distance_from_center)

        self.compute_fiber_list(centers=centers)

    def compute_centers(self, distance_from_center="not-fused") -> None:
        """
        Computing the core center with a a certain distance from the origin  (0, 0).

        :param      distance_from_center:  The distance from center
        :type       distance_from_center:  float
        """
        if distance_from_center == "not-fused":
            factor = numpy.sqrt(2 / (1 - numpy.cos(numpy.deg2rad(self.delta_angle))))
            distance_from_center = factor * self.fiber_radius

        first_core = Point(position=[0, distance_from_center])

        return [first_core.rotate(angle=angle, origin=[0, 0]) for angle in self.angle_list]

    def plot(self,
            show_fibers: bool = True,
            show_added: bool = False,
            show_removed: bool = False,
            show_fused: bool = False,
            show_unfused: bool = False) -> SceneList:
        """
        Plot the structure.

        :returns:   Scene
        :rtype:     SceneList
        """
        figure = SceneList(unit_size=(6, 6))

        ax = figure.append_ax(
            x_label=r'x',
            y_label=r'y',
            show_grid=True,
            equal_limits=False,
            equal=True
        )

        if show_fibers:
            for fiber in self.fiber_list:
                fiber._render_on_ax_(ax)

        if show_added:
            for connection in self.connected_fibers:
                connection.added_section._render_on_ax_(ax, facecolor='green')

        if show_removed:
            for connection in self.connected_fibers:
                connection.removed_section._render_on_ax_(ax, facecolor='red')

        if show_fused:
            self.fused_structure._render_on_ax_(ax=ax)

        if show_unfused:
            self.unfused_structure._render_on_ax_(ax=ax)

        return figure

    @property
    def fused_structure(self):
        return utils.Union(*self.fiber_list, self.added_section)

    @property
    def unfused_structure(self):
        return utils.Union(*self.fiber_list)


if __name__ == '__main__':
    ring = FiberRing(
        number_of_fibers=4,
        fiber_radius=62e-6,
        angle_shift=20,
        tolerance_factor=1e-10
    )

    ring.scale_position(0.9)

    ring.init_connected_fibers()

    ring.compute_optimal_structure()

    figure = ring.plot(show_fused=True, show_removed=True, show_added=True)

    figure.show()

# -
