"""
Linux SPI adapter using the spidev package.

Requires:
    pip install adxl355[spi]

Usage:
    from adxl355.adapters.spidev import SpiDevTransport
    transport = SpiDevTransport(bus=0, device=0, max_speed_hz=1000000)
"""

from __future__ import annotations

import time
from typing import Optional

from adxl355.transport import Transport


class SpiDevTransport(Transport):
    """
    SPI transport for ADXL355 using spidev.
    """

    def __init__(
        self,
        bus: int = 0,
        device: int = 0,
        max_speed_hz: int = 1_000_000,
    ) -> None:
        self._bus = bus
        self._device = device
        self._max_speed_hz = max_speed_hz
        self._spi: Optional[object] = None

    def _ensure_open(self) -> object:
        if self._spi is None:
            import spidev  # type: ignore[import-untyped]

            spi = spidev.SpiDev()
            spi.open(self._bus, self._device)
            spi.max_speed_hz = self._max_speed_hz
            spi.mode = 0  # CPOL=0, CPHA=0
            self._spi = spi
        return self._spi

    def read_register(self, reg: int, length: int = 1) -> bytes:
        spi = self._ensure_open()
        # SPI read: send address with bit 7 set (read flag), then dummy bytes
        header = bytes([0x80 | reg])
        dummy = bytes([0x00]) * length
        result = spi.xfer2(list(header + dummy))  # type: ignore[arg-type]
        return bytes(result[1:])

    def write_register(self, reg: int, data: bytes) -> None:
        spi = self._ensure_open()
        # SPI write: send address (bit 7 clear), then data
        header = bytes([reg & 0x7F])
        payload = list(header + data)
        spi.xfer2(payload)

    def delay_ms(self, ms: int) -> None:
        time.sleep(ms / 1000.0)

    def close(self) -> None:
        if self._spi is not None:
            self._spi.close()
            self._spi = None
