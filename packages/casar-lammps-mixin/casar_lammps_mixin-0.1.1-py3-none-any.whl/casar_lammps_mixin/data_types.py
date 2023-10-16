"""Collection of different datatypes relevant to the repository."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple, Union

import numpy as np
import pandas as pd


@dataclass
class BaseDataModel:
    """Represent base model for a LAMMPS component."""

    type: int

    def is_type_of_interest(
        self, types_of_interest: SingleType | MultiTypes | None = None
    ) -> bool:
        """Flag component's type matches the specified types of interest.

        Args:
            types_of_interest: The type(s) of interest to compare

        Returns:
            Bool flag if the component matches the specified type(s)
        """
        if types_of_interest is None:
            return True

        if isinstance(types_of_interest, int):
            return self.type == types_of_interest
        else:
            return self.type in types_of_interest


@dataclass
class AtomData(BaseDataModel):
    """Components of the Atom section of a LAMMPS data file."""

    index: int
    molecule: int
    charge: float
    x: float
    y: float
    z: float

    @classmethod
    def from_atom_line(cls, atom_line: str) -> AtomData:
        """Construct atom data from an atom line.

        Args:
            atom_line: An atom line from a LAMMPS data file

        Returns:
            The AtomData from the line
        """
        split_line = atom_line.strip().split()
        return AtomData(
            index=int(split_line[0]),
            molecule=int(split_line[1]),
            type=int(split_line[2]),
            charge=float(split_line[3]),
            x=float(split_line[4]),
            y=float(split_line[5]),
            z=float(split_line[6]),
        )


@dataclass
class BondData(BaseDataModel):
    """Components of the Bonds section of a LAMMPS data file."""

    atom1_index: int
    atom2_index: int
    index: int | None = None

    def __str__(self) -> str:  # noqa: D105
        return f"{self.index:>6d}{self.type:>3d}{self.atom1_index:>7d}{self.atom2_index:>7d}\n"  # noqa: E501

    @classmethod
    def from_bonds_line(cls, bonds_line: str) -> BondData:
        """Construct bond data from a bonds line.

        Args:
            bonds_line: An bonds line from a LAMMPS data file

        Returns:
            The BondData from the line
        """
        split_line = [int(comp) for comp in bonds_line.strip().split()]
        return BondData(
            index=split_line[0],
            type=split_line[1],
            atom1_index=split_line[2],
            atom2_index=split_line[3],
        )


@dataclass
class AngleData(BaseDataModel):
    """Components for the Angles section of a LAMMPS data file."""

    atom1_index: int
    center_index: int
    atom2_index: int
    index: int | None = None
    degrees: float | None = None

    def __str__(self) -> str:  # noqa: D105
        return f"{self.index:>6d}{self.type:>3d}{self.atom1_index:>7d}{self.center_index:>7d}{self.atom2_index:>7d}\n"  # noqa: E501

    @classmethod
    def from_angles_line(cls, angles_line: str) -> AngleData:
        """Construct angle data from a angles line.

        Args:
            angles_line: An bonds line from a LAMMPS data file

        Returns:
            The AnglesData from the line
        """
        split_line = [int(comp) for comp in angles_line.strip().split()]
        return AngleData(
            index=split_line[0],
            type=split_line[1],
            atom1_index=split_line[2],
            center_index=split_line[3],
            atom2_index=split_line[4],
        )

    def calculate_deg(self, atoms: pd.DataFrame) -> None:
        """Calculate the angle of the given set of atoms.

        Method from https://stackoverflow.com/questions/35176451/

        Args:
            atoms: A dataframe that references atoms by ID from the Atom section
        """
        # .iloc references the previous row, so subtract 1 for the correct idx
        center_atom = atoms.iloc[self.center_index - 1][["x", "y", "z"]].to_numpy()
        a1_atom = atoms.iloc[self.atom1_index - 1][["x", "y", "z"]].to_numpy()
        a2_atom = atoms.iloc[self.atom2_index - 1][["x", "y", "z"]].to_numpy()

        ba = a1_atom - center_atom
        bc = a2_atom - center_atom

        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc))
        angle = np.arccos(cosine_angle)
        self.degrees = np.degrees(angle)


@dataclass
class DumpLine:
    """Components in a line of a dump file."""

    timestep: int
    id: int
    type: int
    x: float
    y: float
    z: float
    vx: float
    vy: float
    vz: float


@dataclass
class Newt:
    """Newtonian elements to inspect."""

    t2: int
    t1: int
    t2_distance: float
    t1_distance: float


SingleType = int
MultiTypes = Tuple[int, ...]

BondPair = Tuple[int, int]
AnglePoints = Tuple[Union[SingleType, MultiTypes], int, Union[SingleType, MultiTypes]]
EntityInfo = Dict[str, Union[float, int]]
