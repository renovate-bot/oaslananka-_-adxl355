"""Integration tests for ADXL355 device with mock transport."""

import pytest

from adxl355 import ADXL355, Range, PowerMode
from adxl355.errors import DeviceNotFoundError, InvalidConfigurationError
from adxl355.registers import Register
from adxl355.testing import MockTransport


@pytest.fixture
def mock_device() -> ADXL355:
    """Create an ADXL355 instance with a mock transport that passes probe."""
    transport = MockTransport()
    transport.set_identity_ok()
    dev = ADXL355(transport)
    dev.probe()
    return dev


class TestProbe:
    def test_successful_probe(self) -> None:
        transport = MockTransport()
        transport.set_identity_ok()
        dev = ADXL355(transport)
        assert dev.probe() is True

    def test_probe_bad_device(self) -> None:
        transport = MockTransport()  # Identity NOT set
        dev = ADXL355(transport)
        with pytest.raises(DeviceNotFoundError):
            dev.probe()

    def test_probe_wrong_id(self) -> None:
        transport = MockTransport()
        transport.set_register(Register.DEVID_AD, 0x00)  # wrong
        transport.set_register(Register.DEVID_MST, 0x1D)
        transport.set_register(Register.PARTID, 0xED)
        dev = ADXL355(transport)
        with pytest.raises(DeviceNotFoundError):
            dev.probe()


class TestRange:
    def test_set_range_writes_register(self, mock_device: ADXL355) -> None:
        mock_device.set_range(Range.G8)
        transport = mock_device._transport
        # Verify a write to RANGE register happened
        writes = [c for c in transport.calls if c["is_write"] and c["reg"] == Register.RANGE]
        assert len(writes) >= 1

    def test_set_invalid_range(self, mock_device: ADXL355) -> None:
        with pytest.raises(InvalidConfigurationError):
            mock_device.set_range(99)  # type: ignore[arg-type]

    def test_get_range(self, mock_device: ADXL355) -> None:
        mock_device.set_range(Range.G2)
        assert mock_device.get_range() == Range.G2

        mock_device.set_range(Range.G8)
        assert mock_device.get_range() == Range.G8


class TestPowerMode:
    def test_set_power_mode(self, mock_device: ADXL355) -> None:
        # Should not raise
        mock_device.set_power_mode(PowerMode.MEASUREMENT)
        mock_device.set_power_mode(PowerMode.STANDBY)


class TestReadRaw:
    def test_read_raw(self, mock_device: ADXL355) -> None:
        transport = mock_device._transport
        transport.set_xyz_raw(x=100, y=-200, z=300)
        raw = mock_device.read_raw()
        assert raw.x == 100, f"Expected x=100, got {raw.x}"
        assert raw.y == -200, f"Expected y=-200, got {raw.y}"
        assert raw.z == 300, f"Expected z=300, got {raw.z}"


class TestReadAcceleration:
    def test_read_g(self, mock_device: ADXL355) -> None:
        transport = mock_device._transport
        transport.set_xyz_raw(x=524287, y=0, z=-524288)
        accel = mock_device.read_acceleration_g()
        assert accel.x > 0
        assert accel.y == 0.0
        assert accel.z < 0

    def test_read_mps2(self, mock_device: ADXL355) -> None:
        transport = mock_device._transport
        transport.set_xyz_raw(x=100000, y=0, z=0)
        accel = mock_device.read_acceleration_mps2()
        assert accel.x != 0.0
        assert accel.y == 0.0
        assert accel.z == 0.0


class TestStatus:
    def test_read_status(self, mock_device: ADXL355) -> None:
        transport = mock_device._transport
        transport.set_register(Register.STATUS, 0x08)  # DATA_RDY
        status = mock_device.read_status()
        assert status & 0x08


class TestReset:
    def test_reset(self, mock_device: ADXL355) -> None:
        mock_device.reset()
        transport = mock_device._transport
        writes = [c for c in transport.calls if c["is_write"] and c["reg"] == Register.RESET]
        assert len(writes) >= 1


class TestTemperature:
    def test_temperature_raw(self, mock_device: ADXL355) -> None:
        transport = mock_device._transport
        transport.set_register(Register.TEMP2, 0x01)
        transport.set_register(Register.TEMP1, 0x90)
        raw = mock_device.read_temperature_raw()
        assert raw == 0x0190

    def test_temperature_c(self, mock_device: ADXL355) -> None:
        transport = mock_device._transport
        transport.set_register(Register.TEMP2, 0x00)
        transport.set_register(Register.TEMP1, 0x00)
        temp = mock_device.read_temperature_c()
        assert temp == 25.0  # 0/100 + 25
