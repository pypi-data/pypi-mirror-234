#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused


class Fused4(BaseFused):
    n_fibers = 4

    def __init__(self,
                 fiber_radius: float,
                 index: float,
                 fusion_degree: float = None,
                 core_position_scrambling: float = 0):

        if fusion_degree is None:
            fusion_degree = 0.8

        super().__init__(index=index)

        FusionRange = [0, 1]
        assert FusionRange[0] <= fusion_degree <= FusionRange[1], f"Fusion degree has to be in the range {FusionRange}"

        self.add_fiber_ring(
            number_of_fibers=4,
            fusion_degree=fusion_degree,
            fiber_radius=fiber_radius
        )

        self.init_connected_fibers()

        self.compute_optimal_structure()

        self.compute_core_position()

        self.randomize_core_position(randomize_position=core_position_scrambling)


if __name__ == '__main__':
    instance = Fused4(
        fiber_radius=62.5, 
        fusion_degree=0.6, 
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
