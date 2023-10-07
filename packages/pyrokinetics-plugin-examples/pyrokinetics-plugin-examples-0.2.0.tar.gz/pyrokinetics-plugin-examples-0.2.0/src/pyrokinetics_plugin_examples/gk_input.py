"""Defines a mock Pyrokinetics GKInput reader."""

from pathlib import Path
from typing import ClassVar, NoReturn

from pyrokinetics.file_utils import FileReader
from pyrokinetics.gk_code import GKInput

from .utils import verify

__all__ = ["make_gk_input", "MyGKInput"]


class MyGKInput(GKInput, FileReader, file_type="_test", reads=GKInput):
    code_type: ClassVar[str] = "_test"

    def read_from_file(self, filename: Path) -> GKInput:
        """Raises exception if reading wrong file, returns empty GKInput."""
        self.verify_file_type(filename)
        return make_gk_input()

    def verify_file_type(self, filename: Path) -> None:
        """Raise exception if not passed a "Hello world!" file."""
        verify(filename)

    def read_str(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def read_dict(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def write(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def set(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def is_nonlinear(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def add_flags(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def get_local_geometry(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def get_local_species(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError

    def get_numerics(self) -> NoReturn:
        """Not implemented."""
        raise NotImplementedError


def make_gk_input() -> GKInput:
    """Creates a Pyrokinetics GKInput object."""
    return MyGKInput()
