from .geometry import Geometry
from .buffer import Circle, Point
from .background import BackGround
from .instances.Fused1 import Fused1
from .instances.Fused2 import Fused2
from .instances.Fused3 import Fused3
from .instances.Fused4 import Fused4
from .instances.Fused5 import Fused5
from .instances.Fused6 import Fused6
from .instances.Fused7 import Fused7
from .instances.Fused10 import Fused10
from .instances.Fused12 import Fused12
from .instances.Fused19 import Fused19
from FiberFusing import Circle
from .instances.scaling_photonic_lantern_10 import FusedScalingPhotonicLantern10
from .instances.mode_groupe_pl_6 import FusedModeGroupePhotonicLantern6

import numpy
from dataclasses import dataclass

micro = 1e-6


@dataclass
class OpticalStructure():
    name: str
    """ Name of the structure """
    index: float
    """ Refractive index of the structure """
    radius: float
    """ Radius of the circle representing the slice of the structure """
    position: tuple
    """ Center position of the circle """
    is_graded: bool = False
    """ True if the structure is refractive index graded """
    delta_n: float = None
    """ Delta refractvive index of the grading """

    def __post_init__(self) -> None:
        self.polygon = Circle(position=self.position, radius=self.radius)

    def compute_index_from_NA(self) -> float:
        index = numpy.sqrt(self.NA**2 + self.exterior_structure.index**2)

        return index

    def get_V_number(self, wavelength: float) -> float:
        delta_index = numpy.sqrt(self.index**2 - self.exterior_structure.index**2)

        V = 2 * numpy.pi / wavelength * delta_index * self.radius

        return V


# -
