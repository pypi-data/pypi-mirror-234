#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class Fused12(BaseFused):
    n_fibers = 12

    def __init__(self,
                 fiber_radius: float,
                 index: float,
                 scale_down: float = 1,
                 core_position_scrambling: float = 0):

        super().__init__(index=index)

        self.add_fiber_ring(
            number_of_fibers=3,
            fusion_degree=0,
            fiber_radius=fiber_radius
        )

        self.add_fiber_ring(
            number_of_fibers=9,
            fusion_degree=0,
            scale_position=1.05,
            fiber_radius=fiber_radius,
            angle_shift=20
        )

        self.init_connected_fibers()

        self.randomize_core_position(randomize_position=core_position_scrambling)

        self.scale_position(factor=scale_down)


if __name__ == '__main__':
    instance = Fused12(
        fiber_radius=62.5,
        index=1,
        scale_down=1
    )

    figure = instance.plot(
        show_structure=False,
        show_fibers=True,
        show_cores=False
    )

    figure.show()

    # -
