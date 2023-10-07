"""
2x2 Clad
========
"""

from FiberFusing import Fused2

clad = Fused2(
    fiber_radius=62.5e-6,
    fusion_degree=0.3,
    index=1.4444,
    core_position_scrambling=0
)

figure = clad.plot()

figure.show()


# -
