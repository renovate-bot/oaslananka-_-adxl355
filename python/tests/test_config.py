"""Tests for configuration API."""

import pytest

from adxl355 import ADXL355, Range, ODR
from adxl355.testing import MockTransport


class TestODR:
    def test_set_odr(self) -> None:
        transport = MockTransport()
        transport.set_identity_ok()
        dev = ADXL355(transport)
        dev.probe()

        dev.set_odr(ODR.HZ_125)
        # Should not raise
        assert True

    def test_set_invalid_odr(self) -> None:
        transport = MockTransport()
        transport.set_identity_ok()
        dev = ADXL355(transport)
        dev.probe()

        with pytest.raises(Exception):
            dev.set_odr(99)  # type: ignore[arg-type]
