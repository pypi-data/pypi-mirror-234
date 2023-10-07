#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import micro


class SMF28(GenericFiber):
    brand = 'Corning'
    model = "SMF28"

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
            radius=8.2 / 2 * micro, 
        )


class HP630(GenericFiber):
    brand = 'Thorlab'
    model = "HP630"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='clad', 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='core', 
            NA=0.13, 
            radius=3.5 / 2 * micro, 
        )


class HI1060(GenericFiber):
    brand = 'Corning'
    model = "HI630"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='clad', 
            index=self.pure_silica_index, 
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='core', 
            NA=0.14, 
            radius=5.3 / 2 * micro, 
        )


if __name__ == '__main__':
    fiber = SMF28(position=(0, 0), wavelength=1550e-9)
    figure = fiber.plot()
    figure.show_colorbar = True
    figure.show()

# -
