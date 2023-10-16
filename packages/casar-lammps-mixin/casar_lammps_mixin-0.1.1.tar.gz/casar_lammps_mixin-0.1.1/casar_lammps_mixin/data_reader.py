"""Read and parse LAMMPS data files for relevant information."""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterator
import pandas as pd
from parse import parse

from casar_lammps_mixin.data_types import (
    AngleData,
    AtomData,
    BondData,
    MultiTypes,
    SingleType,
)
from casar_lammps_mixin.pbc_construct import PBCShiftMixin


def readout_section_lines(
    section_title: str, n_lines: int | None, lines: Iterator[str]
) -> Iterator[str]:
    """Get the lines of a section by its title.

    Args:
        section_title: The title of the section
        n_lines: The number of lines in the section
        lines: The lines of a file

    Yields:
        The lines of the section of interest

    Raises:
        ValueError: If there are no lines in the section to read
    """
    if not n_lines:
        raise ValueError(f"{section_title} section not found")

    for line in lines:
        if section_title in line:
            # Section titles are followed by a blank line
            next(lines)
            for i in range(n_lines):
                yield next(lines)


@dataclass
class LAMMPSData(PBCShiftMixin):
    """Access the information of a LAMMPS data file."""

    filepath: Path
    atoms: int | None = None
    bonds: int | None = None
    angles: int | None = None
    atom_types: int | None = None
    bond_types: int | None = None
    angle_types: int | None = None
    xlo: float | None = None
    ylo: float | None = None
    zlo: float | None = None
    xhi: float | None = None
    yhi: float | None = None
    zhi: float | None = None
    xy: float | None = None
    xz: float | None = None
    yz: float | None = None

    def __str__(self) -> str:  # noqa: D105
        content = ""
        if self.atoms:
            content += f"{self.atoms} atoms\n"
        if self.bonds:
            content += f"{self.bonds} bonds\n"
        if self.angles:
            content += f"{self.angles} angles\n"
        if self.atom_types:
            content += f"{self.atom_types} atom types\n"
        if self.bond_types:
            content += f"{self.bond_types} bond types\n"
        if self.angle_types:
            content += f"{self.angle_types} angle types\n"
        if (self.xlo and self.xhi) is not None:
            content += f"{self.xlo} {self.xhi} xlo xhi\n"
        if (self.ylo and self.yhi) is not None:
            content += f"{self.ylo} {self.yhi} ylo yhi\n"
        if (self.zlo and self.zhi) is not None:
            content += f"{self.zlo} {self.zhi} zlo zhi\n"
        if (self.xy and self.xz and self.yz) is not None:
            content += f"{self.xy} {self.xz} {self.yz} xy xz yz\n"

        return content

    @classmethod
    def from_local_lammps_data_file(cls, filepath: Path) -> LAMMPSData:
        """Construct LAMMPSDataReader from a local file.

        Assume that the system info is defined in the first 200 lines of the file.

        Args:
            filepath: Local path to a .lammps file

        Returns:
            The LAMMPSDataReader

        Raises:
            ValueError: If the provided file doesn't have a .data extension
        """
        if filepath.suffix != ".data":
            raise ValueError("File provided is not a LAMMPS data file.")
        lammps_data_reader = LAMMPSData(filepath=filepath)

        for line in open(filepath, "r").readlines()[:200]:
            lammps_data_reader.parse_for_info(line)

        return lammps_data_reader

    def parse_for_info(self, line: str) -> None:
        """Parse a line for relevant.

        Args:
            line: A string to parse
        """
        if "atoms" in line:
            result = parse("{atoms} atoms", line.strip())
            self.atoms = int(result["atoms"])
        elif "bonds" in line:
            result = parse("{bonds} bonds", line.strip())
            self.bonds = int(result["bonds"])
        elif "angles" in line:
            result = parse("{angles} angles", line.strip())
            self.angles = int(result["angles"])
        elif "atom types" in line:
            result = parse("{atom_types} atom types", line.strip())
            self.atom_types = int(result["atom_types"])
        elif "bond types" in line:
            result = parse("{bond_types} bond types", line.strip())
            self.bond_types = int(result["bond_types"])
        elif "angle types" in line:
            result = parse("{angle_types} angle types", line.strip())
            self.angle_types = int(result["angle_types"])
        elif "xlo xhi" in line:
            result = parse("{xlo} {xhi} xlo xhi", str.join(" ", line.split()))
            self.xlo = float(result["xlo"])
            self.xhi = float(result["xhi"])
        elif "ylo yhi" in line:
            result = parse("{ylo} {yhi} ylo yhi", str.join(" ", line.split()))
            self.ylo = float(result["ylo"])
            self.yhi = float(result["yhi"])
        elif "zlo zhi" in line:
            result = parse("{zlo} {zhi} zlo zhi", str.join(" ", line.split()))
            self.zlo = float(result["zlo"])
            self.zhi = float(result["zhi"])
        elif "xy xz yz" in line:
            result = parse("{xy} {xz} {yz} xy xz yz", str.join(" ", line.split()))
            self.xy = float(result["xy"])
            self.xz = float(result["xy"])
            self.yz = float(result["xy"])

    def read_lmps_lines(self) -> Iterator[str]:
        """Read the lines in the LAMMPS data file.

        Yields:
            A line of the file
        """
        with open(self.filepath, "r") as f:
            yield from f.readlines()

    def readout_atoms(
        self, types: SingleType | MultiTypes | None = None
    ) -> Iterator[AtomData]:
        """Get the lines of the atoms section.

        Args:
            types: Atom types of interest to readout. If None, will readout all atoms.

        Yields:
            The components of an atomline as AtomData
        """
        for atom_line in readout_section_lines(
            "Atoms", self.atoms, self.read_lmps_lines()
        ):
            atom = AtomData.from_atom_line(atom_line)
            if atom.is_type_of_interest(types):
                yield atom

    def readout_bonds(
        self, types: SingleType | MultiTypes | None = None
    ) -> Iterator[BondData]:
        """Get the lines of the bonds section.

        Args:
            types: Bond types of interest to readout. If None, will readout all bonds.

        Yields:
            The components of a bondline as BondData
        """
        for bonds_line in readout_section_lines(
            "Bonds", self.bonds, self.read_lmps_lines()
        ):
            bond = BondData.from_bonds_line(bonds_line)
            if bond.is_type_of_interest(types):
                yield bond

    def readout_angles(
        self, types: SingleType | MultiTypes | None = None
    ) -> Iterator[AngleData]:
        """Get the lines of the angles section.

        Args:
            types: Angle types of interest to readout. If None, will readout all angles.

        Yields:
            The components of a bondline as AngleData
        """
        for angles_line in readout_section_lines(
            "Angles", self.angles, self.read_lmps_lines()
        ):
            angle = AngleData.from_angles_line(angles_line)
            if angle.is_type_of_interest(types):
                yield angle

    @property
    def has_3d_box(self) -> bool:
        """Flag if the the system has 3D box information defined.

        Returns:
            True, if the system has defined 3D box information
        """
        x_dims = (self.xlo and self.xhi) is not None
        y_dims = (self.ylo and self.yhi) is not None
        z_dims = (self.zlo and self.zhi) is not None
        return all([x_dims, y_dims, z_dims])

    @property
    def has_3d_tilt(self) -> bool:
        """Flag if the the system has 3D tilt information defined.

        Returns:
            True, if the system has defined 3D tilt information
        """
        return all([self.xy, self.xz, self.xz])

    def image_by_symmetry(self, reference: pd.DataFrame) -> pd.DataFrame:
        """Determine if the simulation box is orthogonal or orthoclinic.

        Args:
            reference: The dataframe from which positions are referenced

        Returns:
            A dataframe with the reference and its images in all dimensions

        Raises:
            ValueError: if the system has no 3D simulation box information
        """
        if not self.has_3d_box:
            raise ValueError("Can't perform images without complete 3D information.")

        if self.has_3d_tilt:
            # This means there is a tilt factor transforming an orthogonal system to a
            # parallelipiped. So, create images according to orthoclinic shifts.
            return self.combine_triclinic_shifts(reference)
        else:
            # There are no tilt factors in the system. So, create images according to
            # orthogonal shfits.
            return self.combine_ortho_shifts(reference)

    def combine_ortho_shifts(self, reference: pd.DataFrame) -> pd.DataFrame:
        """Combine all orthogonal shifts.

        Args:
            reference: The dataframe from which positions are referenced

        Returns:
            A dataframe with the reference and its images in all dimensions
        """
        assert self.xhi is not None and self.xlo is not None
        lx = self.xhi - self.xlo
        assert self.yhi is not None and self.ylo is not None
        ly = self.yhi - self.ylo
        assert self.zhi is not None and self.zlo is not None
        lz = self.zhi - self.zlo

        comb1 = pd.concat(
            [
                reference,
                self.translate_x(df=reference, shift=lx),
                self.translate_x(df=reference, shift=-lx),
            ]
        )
        comb2 = pd.concat(
            [
                comb1,
                self.translate_y(df=comb1, shift=ly),
                self.translate_y(df=comb1, shift=-ly),
            ]
        )
        comb3 = pd.concat(
            [
                comb2,
                self.translate_z(df=comb2, shift=lz),
                self.translate_z(df=comb2, shift=-lz),
            ]
        )
        return comb3

    def combine_triclinic_shifts(self, reference: pd.DataFrame) -> pd.DataFrame:
        """Combine all orthogonal shifts.

        Args:
            reference: The dataframe from which positions are referenced

        Returns:
            A dataframe with the reference and its images in all dimensions
        """
        assert self.xhi is not None and self.xlo is not None
        lx = self.xhi - self.xlo
        assert self.yhi is not None and self.ylo is not None
        ly = self.yhi - self.ylo
        assert self.zhi is not None and self.zlo is not None
        lz = self.zhi - self.zlo

        comb1 = pd.concat(
            [
                reference,
                self.translate_x(df=reference, shift=lx),
                self.translate_x(df=reference, shift=-lx),
            ]
        )
        assert self.xy is not None
        comb2 = pd.concat(
            [
                comb1,
                self.translate_tilty(df=comb1, shift_y=ly, shift_xy=self.xy),
                self.translate_tilty(df=comb1, shift_y=-ly, shift_xy=-self.xy),
            ]
        )
        assert self.xz is not None and self.yz is not None
        comb3 = pd.concat(
            [
                comb2,
                self.translate_tiltz(
                    df=comb2, shift_z=lz, shift_xz=self.xz, shift_yz=self.yz
                ),
                self.translate_tiltz(
                    df=comb2, shift_z=-lz, shift_xz=-self.xz, shift_yz=-self.yz
                ),
            ]
        )
        return comb3
