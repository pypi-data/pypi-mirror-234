"""
7x7 Clad
========
"""

from FiberFusing import Fused7

clad = Fused7(
    fiber_radius=62.5e-6,
    fusion_degree=0.6,
    index=1.4444,
    core_position_scrambling=0
)

figure = clad.plot()

figure.show()


# -
