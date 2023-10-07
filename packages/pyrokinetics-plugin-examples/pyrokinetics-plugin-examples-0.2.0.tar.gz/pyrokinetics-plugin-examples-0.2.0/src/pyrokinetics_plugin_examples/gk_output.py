"""Defines a mock Pyrokinetics GKOutput reader."""

from pathlib import Path

import numpy as np
from pyrokinetics.file_utils import FileReader
from pyrokinetics.gk_code.gk_output import Coords, GKOutput
from pyrokinetics.normalisation import SimulationNormalisation

from .utils import verify

__all__ = ["make_gk_output", "GKOutputReader"]


def make_gk_output(norm: SimulationNormalisation) -> GKOutput:
    """Returns a mostly empty GKOutput."""
    coords = Coords(
        kx=np.array([0.0]),
        ky=np.array([0.0]),
        time=np.array([0.0]),
        species=["electron", "ion"],
    )
    return GKOutput(coords=coords, norm=norm, gk_code="_test")


class GKOutputReader(FileReader, file_type="_test", reads=GKOutput):
    def read_from_file(
        self, filename: Path, norm: SimulationNormalisation, **_
    ) -> GKOutput:
        """Raises exception if reading wrong file, returns empty GKOutput."""
        self.verify_file_type(filename)
        return make_gk_output(norm)

    def verify_file_type(self, filename: Path) -> None:
        """Raise exception if not passed a "Hello world!" file."""
        verify(filename)
