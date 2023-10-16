#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import micro


class FiberCoreA(GenericFiber):
    brand = 'FiberCore'
    model = 'PS1250/1500'
    note = "Boron Doped Photosensitive Fiber"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='clad', 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='core', 
            NA=0.12, 
            radius=8.8 / 2 * micro, 
        )


class FiberCoreB(GenericFiber):
    brand = 'FiberCore'
    model = 'SM1250'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='clad', 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='core', 
            NA=0.12, 
            radius=9.0 / 2 * micro, 
        )


if __name__ == '__main__':
    fiber = FiberCoreA(position=(0, 0), wavelength=1550e-9)
    fiber.plot().show()

# -
