#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import OpticalStructure, micro


class DCF13(GenericFiber):
    brand = "Thorlabs"
    model = "DCF13"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad', 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad', 
            NA=0.2, 
            radius=19.9 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core', 
            NA=0.12, 
            radius=105.0 / 2 * micro, 
        )


if __name__ == '__main__':
    fiber = DCF13(position=(0, 0), wavelength=1550e-9)
    fiber.plot().show()

# -
