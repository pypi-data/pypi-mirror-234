#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber


class CustomFiber(GenericFiber):
    def __init__(self, wavelength: float, position: tuple = (0, 0)):
        super().__init__(wavelength=wavelength, position=position)

        self.add_air()


if __name__ == '__main__':
    fiber = CustomFiber(wavelength=1550e-9)

    fiber.add_silica_pure_cladding()

    fiber.create_and_add_new_structure(name='core', radius=40e-6 / 2, NA=0.115)

    fiber.create_and_add_new_structure(name='core', radius=4.1e-6, NA=0.13)

    fiber.plot().show()


# -
