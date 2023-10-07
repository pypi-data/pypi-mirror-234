"""Defines a mock Pyrokinetics Equilibrium reader."""

from pathlib import Path

import numpy as np
from pyrokinetics.equilibrium import Equilibrium
from pyrokinetics.file_utils import FileReader
from pyrokinetics.units import ureg as units

from .utils import verify

__all__ = ["make_equilibrium", "EquilibriumReader"]


def make_equilibrium() -> Equilibrium:
    """Creates a fixed Pyrokinetics equilibrium object."""
    # Define default units
    len_units = units.m
    psi_units = units.weber
    F_units = units.m * units.tesla
    FF_prime_units = F_units**2 / units.weber
    p_units = units.pascal
    p_prime_units = units.pascal / units.weber
    q_units = units.dimensionless
    B_units = units.tesla
    I_units = units.ampere

    # Create set of COCOS 11 args
    n_R = 101
    n_Z = 121
    n_psi = 61
    R_max = 5.0
    R_min = 1.0
    Z_max = 3.0
    Z_min = -1.0

    R = np.linspace(R_min, R_max, n_R)
    Z = np.linspace(-2.0, 2.0, n_Z)
    R_axis = 0.5 * (R_max + R_min)
    Z_axis = 0.5 * (Z_max + Z_min)
    radial_grid = np.sqrt((R - R_axis)[:, np.newaxis] ** 2 + (Z - Z_axis) ** 2)
    psi_offset = -5.1
    psi_RZ = 2 * np.pi * (radial_grid) + psi_offset
    psi_axis = np.min(psi_RZ)
    psi_lcfs = np.min(psi_RZ[0])
    a_minor = 0.5 * (R_max - R_min)

    psi = np.linspace(psi_axis, psi_lcfs, n_psi)
    F = psi**2
    F_prime = 2 * psi
    FF_prime = F * F_prime
    p = 3000 + 100 * psi
    p_prime = 100 * np.ones(n_psi)
    q = np.linspace(2.0, 7.0, n_psi)
    R_major = R_axis * np.ones(n_psi)
    r_minor = np.linspace(0, a_minor, n_psi)
    Z_mid = Z_axis * np.ones(n_psi)
    B_0 = 2.5
    I_p = 1e6

    return Equilibrium(
        R=R * len_units,
        Z=Z * len_units,
        psi_RZ=psi_RZ * psi_units,
        psi=psi * psi_units,
        F=psi * F_units,
        FF_prime=FF_prime * FF_prime_units,
        p=p * p_units,
        p_prime=p_prime * p_prime_units,
        q=q * q_units,
        R_major=R_major * len_units,
        r_minor=r_minor * len_units,
        Z_mid=Z_mid * len_units,
        psi_lcfs=psi_lcfs * psi_units,
        a_minor=a_minor * len_units,
        B_0=B_0 * B_units,
        I_p=I_p * I_units,
        eq_type="_test",
    )


class EquilibriumReader(FileReader, file_type="_test", reads=Equilibrium):
    def read_from_file(self, filename: Path) -> Equilibrium:
        """Raises exception if reading wrong file, returns standard Equilibrium."""
        self.verify_file_type(filename)
        return make_equilibrium()

    def verify_file_type(self, filename: Path) -> None:
        """Raise exception if not passed a "Hello world!" file."""
        verify(filename)
