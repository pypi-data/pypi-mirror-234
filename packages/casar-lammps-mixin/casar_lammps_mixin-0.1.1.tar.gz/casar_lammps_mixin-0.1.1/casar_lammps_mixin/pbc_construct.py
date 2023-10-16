"""Assist with creating an expanded system using periodic boundary conditions."""
from __future__ import annotations

import pandas as pd

# from casar_lammps_mixin.data_reader import LAMMPSData


class PBCShiftMixin:
    """A namespace for assisting with periodic boundary conditions."""

    @staticmethod
    def update_df(
        reference: pd.DataFrame,
        dx: pd.Series | None = None,
        dy: pd.Series | None = None,
        dz: pd.Series | None = None,
    ) -> pd.DataFrame:
        """Shift the positions of a given dimension.

        Args:
            reference: The dataframe from which positions are referenced
            dx: The shifted positions in the x-direction
            dy: The shifted positions in the y-direction
            dz: The shifted positions in the z-direction

        Returns:
            A dataframe with shifted positions
        """
        updated = reference.copy()
        if isinstance(dx, pd.Series):
            updated["x"] = dx
        if isinstance(dy, pd.Series):
            updated["y"] = dy
        if isinstance(dz, pd.Series):
            updated["z"] = dz
        return updated

    @classmethod
    def translate_x(cls, df: pd.DataFrame, shift: float) -> pd.DataFrame:
        """Translate in the x-dimension.

        Args:
            df: A dataframe with an "x"-column
            shift: Quantity to shift in the x-direction

        Returns:
            A dataframe that is shifted in the x-direction
        """
        shift = df["x"] + shift
        return cls.update_df(reference=df, dx=shift)

    @classmethod
    def translate_y(cls, df: pd.DataFrame, shift: float) -> pd.DataFrame:
        """Translate in the y-dimension.

        Args:
            df: A dataframe with a "y"-column
            shift: Quantity to shift in the y-direction

        Returns:
            A dataframe that is shifted in the y-direction
        """
        shift = df["y"] + shift
        return cls.update_df(reference=df, dy=shift)

    @classmethod
    def translate_z(cls, df: pd.DataFrame, shift: float) -> pd.DataFrame:
        """Translate in the z-dimension.

        Args:
            df: A dataframe with a "z"-column
            shift: Quantity to shift in the z-direction

        Returns:
            A dataframe that is shifted in the z-direction
        """
        shift = df["z"] + shift
        return cls.update_df(reference=df, dz=shift)

    @classmethod
    def translate_tilty(
        cls, df: pd.DataFrame, shift_y: float, shift_xy: float
    ) -> pd.DataFrame:
        """Translate along the xy-tilt.

        Args:
            df: A dataframe with an "x"- and "y"-column
            shift_y: Quantity to shift in the y-direction
            shift_xy: Quantity to shift the x-direction

        Returns:
            A dataframe that is shifted in the z-direction
        """
        col_shifty = df["y"] + shift_y
        col_shiftx = df["x"] + shift_xy
        return cls.update_df(reference=df, dx=col_shiftx, dy=col_shifty)

    @classmethod
    def translate_tiltz(
        cls, df: pd.DataFrame, shift_z: float, shift_xz: float, shift_yz: float
    ) -> pd.DataFrame:
        """Translate along the xz-tilt.

        Args:
            df: A dataframe with an "x", "y", and "z"-column
            shift_z: Quantity to shift in the z-direction
            shift_xz: Quantity to shift the x-direction
            shift_yz: Quantity to shift the y-direction

        Returns:
            A dataframe that is shifted in the z-direction
        """
        col_shiftz = df["z"] + shift_z
        col_shifty = df["y"] + shift_yz
        col_shiftx = df["x"] + shift_xz
        return cls.update_df(reference=df, dx=col_shiftx, dy=col_shifty, dz=col_shiftz)
