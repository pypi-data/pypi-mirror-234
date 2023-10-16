"""Handler for processing LAMMPS dump files."""
from __future__ import annotations

import random
import time
from collections import defaultdict
from pathlib import Path
from typing import Iterator

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from casar_lammps_mixin.data_types import BondData, DumpLine, Newt


class DumpHandler:
    """Access the information of a .dmp file."""

    def __init__(self, filepath: Path):
        """Initialise by defining a filepath.

        Args:
            filepath: The path to a .dmp file.
        """
        self.filepath = filepath

    def readlines(self) -> Iterator[str]:
        """Read the lines of the .dmp file.

        Yields:
            The stripped line of the .dmp file.
        """
        with open(self.filepath, "r") as f:
            for line in f.readlines():
                yield line.strip()

    def identify_dump_lines(self) -> Iterator[DumpLine]:
        """Get the lines of the Atom section.

        Yields:
            The line of the Atom section as a DumpLine
        """
        lines = self.readlines()
        for line in lines:
            if line == "ITEM: TIMESTEP":
                timestep = int(next(lines))
            elif line == "ITEM: NUMBER OF ATOMS":
                n_atoms = int(next(lines))
            elif line == "ITEM: ATOMS id type x y z vx vy vz":
                for placer in range(n_atoms):
                    line_split = next(lines).split()
                    dumpline = DumpLine(
                        timestep=timestep,
                        id=int(line_split[0]),
                        type=int(line_split[1]),
                        x=float(line_split[2]),
                        y=float(line_split[3]),
                        z=float(line_split[4]),
                        vx=float(line_split[5]),
                        vy=float(line_split[6]),
                        vz=float(line_split[7]),
                    )
                    yield dumpline

    def collect_coreshell_atoms(
        self, bond: BondData | None = None
    ) -> Iterator[DumpLine]:
        """Separate out the core shell atoms.

        Here we're assuming that core and shell atoms are types 3 & 4. If a bond isn't
        provided, then default to collecting all the coreshell atoms.

        Args:
            bond: The data of a given bond

        Yields:
            The line of either a core or shell atom
        """
        print("Collecting coreshell atoms", flush=True)
        start_time = time.time()
        for dumpline in self.identify_dump_lines():
            if dumpline.type in (3, 4):
                if bond:
                    if (dumpline.id == bond.atom1_index) or (
                        dumpline.id == bond.atom2_index
                    ):
                        yield dumpline
                else:
                    yield dumpline
        elapsed = time.time() - start_time
        print(f"Collected coreshells in {elapsed:.1f} seconds")

    @staticmethod
    def pair_coreshell(bond: BondData, coreshell_atoms: pd.DataFrame) -> pd.DataFrame:
        """Merge the core and shell dumplines.

        Args:
            bond: Core-shell bond of interest
            coreshell_atoms: Dataframe of core shell atoms in the dump file

        Returns:
            The dataframe of the core and shell, merged on timestep
        """
        bond_atoms = coreshell_atoms.loc[
            (coreshell_atoms["id"] == bond.atom1_index)
            | (coreshell_atoms["id"] == bond.atom2_index)
        ]
        core = bond_atoms[bond_atoms["type"] == 3].reset_index(drop=True)
        shell = bond_atoms[bond_atoms["type"] == 4].reset_index(drop=True)

        merge = pd.merge(
            core[["timestep", "x", "y", "z"]],
            shell[["timestep", "x", "y", "z"]],
            how="outer",
            on="timestep",
        )
        merge.columns = ["timestep", "c_x", "c_y", "c_z", "s_x", "s_y", "s_z"]
        return merge

    def collect_newts(
        self, bond: BondData, coreshell_atoms: pd.DataFrame
    ) -> Iterator[Newt]:
        """Collect values from t2 and t1 into a Newt.

        Args:
            bond: Core-shell bond of interest
            coreshell_atoms: Dataframe of core shell atoms in the dump file

        Yields:
            The calculated Newt component of a coreshell pair
        """
        df = self.pair_coreshell(bond, coreshell_atoms)
        df["distance"] = np.linalg.norm(
            df[["c_x", "c_y", "c_z"]].values - df[["s_x", "s_y", "s_z"]].values, axis=1
        )

        for i in range(1, df.shape[0]):
            now = df.iloc[i]
            prev = df.iloc[i - 1]
            newt = Newt(
                t2=now["timestep"],
                t1=prev["timestep"],
                t2_distance=now["distance"],
                t1_distance=prev["distance"],
            )
            yield newt

    def calculate_coreshell_props(
        self, bond: BondData, coreshell_atoms: pd.DataFrame
    ) -> pd.DataFrame:
        """Calculate the different core-shell properties.

        Args:
            bond: Core-shell bond of interest
            coreshell_atoms: Dataframe of core shell atoms in the dump file

        Returns:
            The calculated properties between a core-shell, as a Newt
        """
        df = pd.DataFrame(self.collect_newts(bond, coreshell_atoms))
        print(
            f"Calculating core-shell stats of Bond {bond.index} for {df.shape[0]} timesteps",  # noqa: E501
            flush=True,
        )

        # Calculate the velocity
        delta = df["t2_distance"] - df["t1_distance"]
        dt = 0.0002 * 1000  # from ps to ns
        df["velocity"] = delta / dt
        # Calculate the kinetic energy
        df["kinetic_energy"] = 1 / 2 * 0.2 * df["velocity"] ** 2

        return df

    def inspect_coreshell(self, bond: BondData, coreshell_atoms: pd.DataFrame) -> None:
        """Plot the different core-shell properties.

        Args:
            bond: Core-shell bond of interest
            coreshell_atoms: Dataframe of core shell atoms in the dump file
        """
        df = self.calculate_coreshell_props(bond, coreshell_atoms)

        plt.figure()
        plt.title(f"{self.filepath}: Bond {bond.index} Distance")
        plt.plot(df["t2"], df["t2_distance"])
        plt.savefig(f"bond{bond.index}_distance.png")

        plt.figure()
        plt.title(f"{self.filepath}: Bond {bond.index} Velocity")
        plt.plot(df["t2"], df["velocity"])
        plt.savefig(f"bond{bond.index}_velocity.png")

        plt.figure()
        plt.title(f"{self.filepath}: Bond {bond.index} Kinetic Energy")
        plt.plot(df["t2"], df["kinetic_energy"])
        plt.savefig(f"bond{bond.index}_kinetic_energy.png")

    @staticmethod
    def randomly_select_bonds(
        n_bonds: int, coreshell_bonds: list[BondData], seed: int | None = None
    ) -> list[int]:
        """Randomly select n bonds.

        An interesting set [103, 326, 193, 175, 430] indexed from corehell_bonds

        Args:
            n_bonds: The number of bonds to randomly select
            coreshell_bonds: The list of bonds used for random selection. This is
                             typically generated from the Bond section of a LAMMPS data
                             file.
            seed: Seed the randomizer with a specified int

        Returns:
            The randomly selected index of the bond in the bonds list.
        """
        if seed:
            random.seed(seed)
        bond_sample = random.sample(range(len(coreshell_bonds)), n_bonds)
        return sorted(bond_sample)

    def summarize_coreshell_props(
        self,
        subset_bonds: list[int],
        coreshell_bonds: list[BondData],
        coreshell_atoms: pd.DataFrame,
    ) -> defaultdict[int, pd.DataFrame]:
        """Summarize the calculated properties of randomly selected bonds.

        Args:
            subset_bonds: The list of bond indices from the bonds list
            coreshell_bonds: The list of bonds used for random selection. This is
                             typically generated from the Bond section of a LAMMPS data
                             file.
            coreshell_atoms: Dataframe of core shell atoms in the dump file

        Returns:
            A dataframe summarizing the calculated properties of randomly selected bonds
        """
        summary: defaultdict[int, pd.DataFrame] = defaultdict()
        for idx in subset_bonds:
            bond = coreshell_bonds[idx]
            summary[idx] = self.calculate_coreshell_props(bond, coreshell_atoms)

        return summary
