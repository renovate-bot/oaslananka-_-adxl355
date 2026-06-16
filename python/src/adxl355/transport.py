"""Abstract transport interface for ADXL355 communication."""

from typing import Protocol, runtime_checkable


@runtime_checkable
class Transport(Protocol):
    """
    Abstract bus transport for ADXL355 communication.

    Implementations wrap SPI, I2C, or mock backends.
    """

    def read_register(self, reg: int, length: int = 1) -> bytes:
        """Read `length` bytes starting at register address `reg`."""
        ...

    def write_register(self, reg: int, data: bytes) -> None:
        """Write `data` bytes starting at register address `reg`."""
        ...

    def delay_ms(self, ms: int) -> None:
        """Blocking delay in milliseconds (optional)."""
        ...
