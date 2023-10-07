"""Defines a mock Pyrokinetics Kinetics reader."""

from pathlib import Path

from pyrokinetics.file_utils import FileReader
from pyrokinetics.kinetics import Kinetics

from .utils import verify

__all__ = ["make_kinetics", "KineticsReader"]


def make_kinetics() -> Kinetics:
    """Creates an empty Pyrokinetics Kinetics object."""
    return Kinetics(kinetics_type="_test")


class KineticsReader(FileReader, file_type="_test", reads=Kinetics):
    def read_from_file(self, filename: Path) -> Kinetics:
        """Raises exception if reading wrong file, returns empty Kinetics."""
        self.verify_file_type(filename)
        return make_kinetics()

    def verify_file_type(self, filename: Path) -> None:
        """Raise exception if not passed a "Hello world!" file."""
        verify(filename)
