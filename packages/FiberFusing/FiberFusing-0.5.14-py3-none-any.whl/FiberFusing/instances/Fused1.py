#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.baseclass import BaseFused
import logging


class Fused1(BaseFused):
    n_fibers = 1

    def __init__(self,
                 fiber_radius: float,
                 index: float,
                 core_position_scrambling: float = 0,
                 fusion_degree: float = None):

        if fusion_degree is not None:
            logging.warning(f"This instance: {self.__class__} do not take fusion_degree as argument.")

        super().__init__(index=index)

        self.add_center_fiber(fiber_radius=fiber_radius)

        self._clad_structure = self.fiber_list[0]

        self.randomize_core_position(randomize_position=core_position_scrambling)


if __name__ == '__main__':
    instance = Fused1(
        fiber_radius=62.5e-6,
        index=1,
        core_position_scrambling=2e-6
    )

    figure = instance.plot(
        show_structure=False,
        show_fibers=True,
        show_cores=True
    )

    figure.show()
