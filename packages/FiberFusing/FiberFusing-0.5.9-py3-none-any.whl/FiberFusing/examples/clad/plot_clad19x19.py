"""
19x19 Clad
==========
"""

from FiberFusing import Fused19

clad = Fused19(
    fiber_radius=62.5e-6,
    scale_down=1.0,
    index=1.4444,
    core_position_scrambling=0
)

figure = clad.plot()

figure.show()


# -
