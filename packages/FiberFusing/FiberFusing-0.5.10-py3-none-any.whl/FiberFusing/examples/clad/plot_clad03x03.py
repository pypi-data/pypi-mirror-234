"""
3x3 Clad
========
"""

from FiberFusing import Fused3

clad = Fused3(
    fiber_radius=62.5,
    fusion_degree=0.3,
    index=1.4444,
    core_position_scrambling=0
)

figure = clad.plot()

figure.show()


# -
