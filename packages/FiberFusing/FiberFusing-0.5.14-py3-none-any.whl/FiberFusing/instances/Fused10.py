#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused
import logging


class Fused10(BaseFused):
    n_fibers = 10

    def __init__(self,
                 fiber_radius: float,
                 index: float,
                 fusion_degree: float = None,
                 core_position_scrambling: float = 0):

        if fusion_degree is not None:
            logging.warning(f"This instance: {self.__class__} do not take fusion_degree as argument.")

        super().__init__(index=index)

        self.add_fiber_ring(
            number_of_fibers=7,
            fiber_radius=fiber_radius,
            scale_position=1.3
        )

        self.add_fiber_ring(
            number_of_fibers=3,
            fiber_radius=fiber_radius,
            scale_position=1,
            angle_shift=25,
            position_shift=[0, 0]
        )

        self.init_connected_fibers()

        self.compute_core_position()

        self.randomize_core_position(randomize_position=core_position_scrambling)


if __name__ == '__main__':
    instance = Fused10(
        fiber_radius=62.5e-6,
        index=1
    )

    figure = instance.plot(
        show_structure=True,
        show_fibers=True,
        show_cores=True,
        show_added=False
    )

    figure.show()

# -
