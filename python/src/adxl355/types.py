"""ADXL355 data types."""

from dataclasses import dataclass


@dataclass(frozen=True)
class RawXYZ:
    """Raw 20-bit acceleration data (sign-extended to int)."""

    x: int
    y: int
    z: int


@dataclass(frozen=True)
class AccelXYZ:
    """Acceleration in floating-point units."""

    x: float
    y: float
    z: float
