#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import OpticalStructure, micro


class GradientCore(GenericFiber):
    # Fiber from https://www.nature.com/articles/s41598-018-27072-2

    def __init__(self, *args, core_radius, delta_n, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad', 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        if isinstance(delta_n, str):
            factor = float(delta_n.strip('%')) / 100
            delta_n = self.pure_silica_index * factor

        self.create_and_add_new_structure(
            name='core', 
            is_graded=True, 
            delta_n=delta_n, 
            radius=core_radius, 
            index=self.pure_silica_index
        )


if __name__ == '__main__':
    fiber = GradientCore(wavelength=1550e-9, core_radius=40e-6, delta_n='5%', position=(0, 0))
    figure = fiber.plot().show()

# -
