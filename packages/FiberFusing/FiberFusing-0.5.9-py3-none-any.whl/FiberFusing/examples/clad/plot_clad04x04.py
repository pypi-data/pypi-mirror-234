"""
4x4 Clad
========
"""

from FiberFusing import Fused4

clad = Fused4(
    fiber_radius=62.5e-6,
    fusion_degree=0.8,
    index=1.4444,
    core_position_scrambling=0
)

figure = clad.plot()

figure.show()

# -
