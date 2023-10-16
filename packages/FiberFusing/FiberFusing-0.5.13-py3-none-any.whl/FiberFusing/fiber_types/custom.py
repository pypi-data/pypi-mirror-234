#!/usr/bin/env python
# -*- coding: utf-8 -*-

from FiberFusing.fiber_base_class import GenericFiber
from FiberFusing import micro


class DCF1300S_20(GenericFiber):
    brand = "COPL"
    model = "DCF1300S_20"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.11,
            radius=19.9 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.12,
            radius=9.2 / 2 * micro,
        )


class DCF1300S_33(GenericFiber):
    brand = "COPL"
    model = "DCF1300S_33"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.11,
            radius=33.0 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.125,
            radius=9.0 / 2 * micro,
        )


class DCF1300S_26(GenericFiber):
    brand = "COPL"
    model = "DCF1300S_26"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.117,
            radius=26.8 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.13,
            radius=9.0 / 2 * micro,
        )


class DCF1300S_42(GenericFiber):
    brand = "COPL"
    model = "DCF1300S_42"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.116,
            radius=42.0 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.13,
            radius=9.0 / 2 * micro,
        )


class F2058L1(GenericFiber):
    brand = "COPL"
    model = "F2058L1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.117,
            radius=19.6 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.13,
            radius=9.0 / 2 * micro,
        )


class F2058G1(GenericFiber):
    brand = "COPL"
    model = "F2058G1"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.115,
            radius=32.3 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.124,
            radius=9.0 / 2 * micro,
        )

        self.initialize_from_OpticalStructures(outer_clad, inner_clad, core)


class F2028M24(GenericFiber):
    model = "F2028M24"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.19,
            radius=14.1 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.11,
            radius=2.3 / 2 * micro,
        )


class F2028M21(GenericFiber):
    model = "F2028M21"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.19,
            radius=17.6 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.11,
            radius=2.8 / 2 * micro,
        )


class F2028M12(GenericFiber):
    model = "F2028M12"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.create_and_add_new_structure(
            name='outer_clad',
            index=self.pure_silica_index,
            radius=62.5 * micro
        )

        self.create_and_add_new_structure(
            name='inner_clad',
            NA=0.19,
            radius=25.8 / 2 * micro
        )

        self.create_and_add_new_structure(
            name='core',
            NA=0.11,
            radius=4.1 / 2 * micro,
        )


if __name__ == '__main__':
    fiber = DCF1300S_33(position=(0, 0), wavelength=155e-9)
    fiber.plot().show()

# -
