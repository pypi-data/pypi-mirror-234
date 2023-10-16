"""Generate Bond and Angle sections of a LAMMPS data file."""
from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from typing import Iterator, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.neighbors import KDTree
from casar_lammps_mixin.data_reader import LAMMPSData

from casar_lammps_mixin.data_types import (
    AngleData,
    AnglePoints,
    BondData,
    BondPair,
    EntityInfo,
    MultiTypes,
    SingleType,
)


@dataclass
class BondGenerator:
    """Generate the Bond section of a LAMMPS data file from the provided atoms.

    Args:
        bond_dict: A dictionary summarizing the bonds to be made for the system
        reference: A dataframe with atomic coordinates of the system
        info: The header info of the LAMMPS system
    """

    bond_dict: dict[BondPair, EntityInfo]
    reference: pd.DataFrame
    info: LAMMPSData

    def subset_single_atom_type(self, type: int, with_images: bool) -> pd.DataFrame:
        """Subset a single atom type.

        Args:
            type: The atom type of interest
            with_images: If True, will include atom images

        Returns:
            A dataframe of subset atoms
        """
        subset = self.reference[self.reference["type"] == type]
        if with_images:
            return self.info.image_by_symmetry(subset).reset_index(drop=True)
        return subset.reset_index(drop=True)

    def create_bond_data(
        self, atom1_type: int, atom2_type: int, cutoff: float
    ) -> Iterator[Tuple[int, int]]:
        """Generate bonds between the two atoms queried from the provided cutoff.

        Args:
            atom1_type: The atom type of the first atom in the bond
            atom2_type: The atom type of the second atom in the bond
            cutoff: The cutoff radius for querying the second atoms in the bond

        Yields:
            The generated bond from the queried cutoff as BondData
        """
        df_atom1 = self.subset_single_atom_type(type=atom1_type, with_images=False)
        df_atom2 = self.subset_single_atom_type(type=atom2_type, with_images=True)

        query = df_atom1[["x", "y", "z"]].to_numpy()
        X = df_atom2[["x", "y", "z"]].to_numpy()
        tree = KDTree(X, leaf_size=2)
        indices = tree.query_radius(query, r=cutoff)
        for atom1_index, atom2_indices in enumerate(indices):
            a1 = int(df_atom1.iloc[atom1_index]["index"])
            for atom2_index in atom2_indices:
                a2 = int(df_atom2.iloc[atom2_index]["index"])
                yield a1, a2

    def generate_bonds(self) -> Iterator[BondData]:
        """Generate all bonds for the Bond section.

        Yields:
            The generated bond from the queried cutoff as BondData
        """
        index = 1
        for (atom1_type, atom2_type), values in self.bond_dict.items():
            for atom1_index, atom2_index in self.create_bond_data(
                atom1_type, atom2_type, cutoff=float(values["cutoff"])
            ):
                yield BondData(
                    type=int(values["bond_type"]),
                    atom1_index=atom1_index,
                    atom2_index=atom2_index,
                    index=index,
                )
                index += 1

    def plot_distributions(self, bonds_dataframe: pd.DataFrame) -> None:
        """Plot the distribution of bond distances.

        Args:
            bonds_dataframe: A dataframe with calculated bond distances
        """
        a1 = self.reference.iloc[bonds_dataframe["atom1_index"] - 1]
        a2 = self.reference.iloc[bonds_dataframe["atom2_index"] - 1]
        bonds_dataframe["distance"] = np.linalg.norm(
            a2[["x", "y", "z"]].values - a1[["x", "y", "z"]].values, axis=1
        )
        for bond_type in bonds_dataframe["type"].unique():
            subset = bonds_dataframe[bonds_dataframe["type"] == bond_type]["distance"]
            plt.figure()
            subset.hist()
            plt.title(f"{self.info.filepath}: Bond {bond_type}")
            plt.savefig(f"bond{bond_type}.png")

    def collect_bond_section(self, checkpoint: bool) -> list[BondData]:
        """Update the data info with the newly generated bonds.

        Args:
            checkpoint: If true, will generate plots of generated bond distances.

        Returns:
            A list of bonds for the Bond section.
        """
        bonds = list(self.generate_bonds())
        df_bonds = pd.DataFrame(bonds)
        self.info.bonds = df_bonds.shape[0]
        self.info.bond_types = len(df_bonds["type"].unique())

        if checkpoint:
            self.plot_distributions(df_bonds)

        return bonds


@dataclass
class AngleGenerator:
    """Generate the Angle section of a LAMMPS data file from the provided atoms.

    Args:
        angle_dict: A dictionary summarizing the angles to be made for the system
        reference: A dataframe with atomic coordinates of the system
        info: The header info of the LAMMPS system
    """

    angle_dict: dict[AnglePoints, EntityInfo]
    reference: pd.DataFrame
    info: LAMMPSData

    def subset_center_atom(self, type: SingleType) -> pd.DataFrame:
        """Subset the center type atoms.

        Args:
            type: The atom type of the center atom in the angle

        Returns:
            A dataframe of center type atoms
        """
        df_center = self.reference[self.reference["type"] == type]
        return df_center

    def subset_end_atom(self, type: SingleType | MultiTypes) -> pd.DataFrame:
        """Subset the atom2 type atoms.

        Args:
            type: The atom type of the second atom in the bond

        Returns:
            A dataframe of atom2 type atoms, including the original positions and
            the images in all dimensions.
        """
        if isinstance(type, int):
            df_end = self.reference[self.reference["type"] == type]
            df_full_end = self.info.image_by_symmetry(df_end)
        else:
            df_end = pd.concat(
                [
                    self.reference[self.reference["type"] == end_type]
                    for end_type in type
                ]
            )
            df_full_end = self.info.image_by_symmetry(df_end)
        return df_full_end

    def group_end(
        self,
        center_type: int,
        end_type: SingleType | MultiTypes,
        cutoff: float,
        group: defaultdict[int, set[int]],
    ) -> defaultdict[int, set[int]]:
        """Generate bonds between the two atoms queried from the provided cutoff.

        Args:
            center_type: The atom type of the center atom in the angle
            end_type: The atom type of the end atom in the angle
            cutoff: The cutoff radius for querying the end atoms in the angle
            group: The dictionary for collecting the queried angles

        Returns:
            The dictionary collecting the queried angles
        """
        df_center = self.subset_center_atom(type=center_type).reset_index(drop=True)
        df_end = self.subset_end_atom(type=end_type).reset_index(drop=True)

        query = df_center[["x", "y", "z"]].to_numpy()
        X = df_end[["x", "y", "z"]].to_numpy()
        tree = KDTree(X, leaf_size=2)
        indices = tree.query_radius(query, r=cutoff)
        for center_index, end_indices in enumerate(indices):
            center_atom = int(df_center.iloc[center_index]["index"])
            for end_index in end_indices:
                end_atom = int(df_end.iloc[end_index]["index"])
                group[center_atom].add(end_atom)

        return group

    def collect_end_groups(
        self,
        center_type: int,
        end1: SingleType | MultiTypes,
        cutoff1: float,
        end2: SingleType | MultiTypes,
        cutoff2: float,
    ) -> defaultdict[int, set[int]]:
        """Group the center atom to its end atoms.

        Args:
            center_type: The atom type of the center atom in the angle
            end1: The atom type of the first end atom(s) in the angle
            cutoff1: The cutoff radius for querying the first end atom(s) in the angle
            end2: The atom type of the second end atom(s) in the angle
            cutoff2: The cutoff radius for querying the second end atom(s) in the angle

        Returns:
            The dictionary of the angle groups
        """
        group: defaultdict[int, set[int]] = defaultdict(set)
        if end1 != end2:
            for end_types, cutoff in zip((end1, end2), (cutoff1, cutoff2)):
                group = self.group_end(center_type, end_types, cutoff, group)
        else:
            group = self.group_end(center_type, end1, cutoff1, group)
        return group

    @staticmethod
    def bond_group_angles(
        center_atom: int, end_atoms: List[int]
    ) -> Iterator[Tuple[int, int, int]]:
        """Generate angles from the bonded groups.

        Args:
            center_atom: Type of the center atom in the angle of interest
            end_atoms: Atom type that makes up end atoms in the angle

        Yields:
            The components of an angle as AngleData
        """
        for end1_atom in end_atoms[:-1]:
            end_atoms.pop(0)
            for end2_atom in end_atoms:
                yield center_atom, end1_atom, end2_atom

    def create_angle_data(
        self,
        center_type: int,
        end1: SingleType | MultiTypes,
        cutoff1: float,
        end2: SingleType | MultiTypes,
        cutoff2: float,
    ) -> Iterator[Tuple[int, int, int]]:
        """Create the angle data for a center atom and its end atoms.

        Args:
            center_type: The atom type of the center atom in the angle
            end1: The atom type of the first end atom(s) in the angle
            cutoff1: The cutoff radius for querying the first end atom(s) in the angle
            end2: The atom type of the second end atom(s) in the angle
            cutoff2: The cutoff radius for querying the second end atom(s) in the angle

        Yields:
            The components of an angle as AngleData
        """
        angle_group = self.collect_end_groups(center_type, end1, cutoff1, end2, cutoff2)
        for center_atom, end_atoms in angle_group.items():
            for bond_group_angle in self.bond_group_angles(
                center_atom, list(end_atoms)
            ):
                yield bond_group_angle

    def generate_angles(self) -> Iterator[AngleData]:
        """Generate the angles for each item in the provided angle dictionary.

        Yields:
            The components of an angle as AngleData
        """
        index = 1
        for (end1_types, center_type, end2_types), values in self.angle_dict.items():
            for center_index, atom1_index, atom2_index in self.create_angle_data(
                center_type=center_type,
                end1=end1_types,
                cutoff1=float(values["cutoff1"]),
                end2=end2_types,
                cutoff2=float(values["cutoff2"]),
            ):
                yield AngleData(
                    type=int(values["angle_type"]),
                    center_index=center_index,
                    atom1_index=atom1_index,
                    atom2_index=atom2_index,
                    index=index,
                )
                index += 1

    def collect_angle_section(self, checkpoint: bool) -> list[AngleData]:
        """Update the data info with the newly generated angles.

        Args:
            checkpoint: If true, will generate plots of generated angles.

        Returns:
            A list of angles for the Angle section.
        """
        angles = list(self.generate_angles())
        df_angles = pd.DataFrame(angles)
        self.info.angles = df_angles.shape[0]
        self.info.angle_types = len(df_angles["type"].unique())

        if checkpoint:
            ...

        return angles
