#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing.fiber_base_class import get_silica_index


class CapillaryTube(GenericFiber):
    def __init__(self, wavelength: float,
                       radius: float,
                       index: float = None,
                       position: tuple = (0, 0)) -> None:

        super().__init__(wavelength=wavelength, position=position)
        self.radius = radius
        self._index = index

        self.initialize()

    def initialize(self) -> None:
        self.create_and_add_new_structure(
            name='clad', 
            index=self.index, 
            radius=self.radius
        )

    @property
    def index(self) -> float:
        if self._index is None:
            raise ValueError("Index hasn't been defined for object")
        return self._index

    @index.setter
    def index(self, value: float) -> None:
        self._index = value
        self.initialize()

    def set_delta_n(self, value: float) -> None:
        self.index = self.pure_silica_index + value


class FluorineCapillaryTube(GenericFiber):
    def __new__(cls, wavelength: float, delta_n: float = -15e-3, **kwargs):
        silica_index = get_silica_index(wavelength=wavelength)

        return CapillaryTube(
            wavelength=wavelength, 
            **kwargs, 
            index=silica_index + delta_n
        )


if __name__ == '__main__':
    fiber = CapillaryTube(position=(0, 0), wavelength=1550e-9, index=1.3, radius=1e-3)
    fiber.plot().show()

# -
