#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class Fused3(BaseFused):
    n_fibers = 3

    def __init__(self,
                 fiber_radius: float,
                 index: float,
                 fusion_degree: float = None,
                 core_position_scrambling: float = 0):

        if fusion_degree is None:
            fusion_degree = 0.8

        super().__init__(index=index)

        assert 0 <= fusion_degree <= 1, "fusion_degree degree has to be in the range [0, 1]"

        self.add_fiber_ring(
            number_of_fibers=3,
            fusion_degree=fusion_degree,
            fiber_radius=fiber_radius
        )

        self.init_connected_fibers()

        self.compute_optimal_structure()

        self.compute_core_position()

        self.randomize_core_position(randomize_position=core_position_scrambling)


if __name__ == '__main__':
    instance = Fused3(
        fiber_radius=62.5, 
        fusion_degree=0.3, 
        index=1
    )

    figure = instance.plot(
        show_structure=True, 
        show_fibers=True, 
        show_cores=False,
        show_added=False
    )

    figure.show()

# -
