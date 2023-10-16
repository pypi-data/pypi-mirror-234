"""Write a LAMMPS data file."""

from __future__ import annotations
from dataclasses import dataclass
from io import TextIOWrapper

import time
from pathlib import Path

import pandas as pd

from casar_lammps_mixin.data_reader import LAMMPSData, readout_section_lines
from casar_lammps_mixin.data_types import (
    AngleData,
    AnglePoints,
    BondData,
    BondPair,
    EntityInfo,
)
from casar_lammps_mixin.section_generators import AngleGenerator, BondGenerator


def write_lammps_datafile(
    filepath: Path,
    checkpoint: bool,
    outpath: Path | None = None,
    create_bonds: dict[BondPair, EntityInfo] | None = None,
    create_angles: dict[AnglePoints, EntityInfo] | None = None,
) -> None:
    """Write a LAMMPS file with an angle section to a .data file.

    Args:
        filepath: Path to a LAMMPS data file with an Atom section
        checkpoint: If true, will calculate distances and angles
        outpath: Name of the file to write with the .data extension
        create_bonds: If provided, will generate bonds for the Bond section
        create_angles: If provided, will generate angles for the Angle section
    """
    print(f"Loaded LAMMPS data file: {filepath}", flush=True)
    start_time = time.time()

    lmp = LAMMPSData.from_local_lammps_data_file(filepath)
    atoms = pd.DataFrame(lmp.readout_atoms())

    if create_bonds:
        bg = BondGenerator(bond_dict=create_bonds, reference=atoms, info=lmp)
        bonds = bg.collect_bond_section(checkpoint)
        print(f"Created {len(bonds)} bonds...", flush=True)
    if create_angles:
        ag = AngleGenerator(angle_dict=create_angles, reference=atoms, info=lmp)
        angles = ag.collect_angle_section(checkpoint)
        print(f"Created {len(angles)} angles...", flush=True)

    print("Writing LAMMPS data file...", flush=True)
    if outpath:
        outh = outpath
    else:
        outh = filepath.with_suffix(".FINAL.data")
    pen = LAMMPSDataWriter(
        outfile=outh,
        file=open(outh, "w"),
        info=lmp,
    )
    pen.header_section(new_info=lmp)
    pen.masses_section()
    pen.atoms_section()
    pen.bonds_section(new_bonds=bonds)
    pen.angles_section(new_angles=angles)
    pen.cs_info_section()
    pen.close_file()

    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"File written in {elapsed_time:.2f} seconds to: {pen.outfile}\n", flush=True)


@dataclass
class LAMMPSDataWriter:
    """Write a LAMMPS data file."""

    outfile: Path
    file: TextIOWrapper
    info: LAMMPSData

    def header_section(self, new_info: LAMMPSData | None = None) -> None:
        """Write the header section of the data file with the info of interest.

        Args:
            new_info: The info to write the header section
        """
        self.file.write("# LAMMPS data file written by LAMMPSDataWriter\n\n")
        if not new_info:
            self.file.write(str(self.info))
        else:
            self.file.write(str(new_info))

    def original_section(self, section_title: str, n_lines: int | None) -> None:
        """Write the section from the orginal data file.

        Args:
            section_title: The title of the section
            n_lines: The number of lines in the section
        """
        for line in readout_section_lines(
            section_title, n_lines, self.info.read_lmps_lines()
        ):
            self.file.write(line)

    def masses_section(self) -> None:
        """Write the masses section of the data file."""
        self.file.write("\nMasses\n\n")
        self.original_section("Masses", self.info.atom_types)

    def atoms_section(self) -> None:
        """Write the atoms section of the data file."""
        self.file.write("\nAtoms\n\n")
        self.original_section("Atoms", self.info.atoms)

    def bonds_section(self, new_bonds: list[BondData] | None = None) -> None:
        """Write the bonds section of the data file.

        Args:
            new_bonds: A list of new bonds to write to the bonds section
        """
        self.file.write("\nBonds\n\n")
        if not new_bonds:
            self.original_section("Bonds", self.info.bonds)
        else:
            for bond in new_bonds:
                self.file.write(str(bond))

    def angles_section(self, new_angles: list[AngleData] | None = None) -> None:
        """Write the angles section of the data file.

        Args:
            new_angles: A list of new angles to write to the angles section
        """
        self.file.write("\nAngles\n\n")
        if not new_angles:
            self.original_section("Angles", self.info.angles)
        else:
            for angle in new_angles:
                self.file.write(str(angle))

    def cs_info_section(self) -> None:
        """Write the CS Info section of the data file."""
        self.file.write("\nCS-Info\n\n")
        for atom in self.info.readout_atoms():
            self.file.write(f"{atom.index:>6d}{atom.molecule:>6d}\n")

    def close_file(self) -> None:
        """Close the file."""
        self.file.close()
