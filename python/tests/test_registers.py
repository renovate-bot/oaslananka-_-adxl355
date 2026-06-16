"""Tests for register definitions and enums."""

from adxl355.registers import Register, Range, PowerMode


class TestRegisterValues:
    def test_devid_ad(self) -> None:
        assert Register.DEVID_AD == 0x00

    def test_reset(self) -> None:
        assert Register.RESET == 0x2F

    def test_xdata3(self) -> None:
        assert Register.XDATA3 == 0x08

    def test_range_register(self) -> None:
        assert Register.RANGE == 0x2C


class TestRangeEnum:
    def test_values(self) -> None:
        assert Range.G2 == 0
        assert Range.G4 == 1
        assert Range.G8 == 2

    def test_members(self) -> None:
        assert len(Range) == 3


class TestPowerMode:
    def test_values(self) -> None:
        assert PowerMode.STANDBY == 0
        assert PowerMode.MEASUREMENT == 1
