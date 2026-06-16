"""Basic ADXL355 read example using mock transport.

Run without hardware::

    python examples/basic_read.py

Replace MockTransport with SpiTransport or I2cTransport for real hardware.
"""

from adxl355 import ADXL355, MockTransport


def main() -> None:
    # Mock transport simulates an ADXL355 with correct device ID
    transport = MockTransport()
    dev = ADXL355(transport)

    # Probe checks DEVID_AD, DEVID_MST, PARTID
    if not dev.probe():
        print("ERROR: Device not found")
        return

    dev.set_range(adxl355.Range.G4)
    dev.set_power_mode(adxl355.PowerMode.MEASUREMENT)

    raw = dev.read_raw()
    accel_g = dev.read_g()
    accel_mps2 = dev.read_mps2()
    temp = dev.read_temperature_c()
    status = dev.read_status()

    print(f"Raw:  x={raw.x:7d}  y={raw.y:7d}  z={raw.z:7d}")
    print(f"Accel (g):     x={accel_g.x:10.6f}  y={accel_g.y:10.6f}  z={accel_g.z:10.6f}")
    print(f"Accel (m/s²):  x={accel_mps2.x:10.6f}  y={accel_mps2.y:10.6f}  z={accel_mps2.z:10.6f}")
    print(f"Temperature: {temp:.2f} °C")
    print(f"Status:  0x{status:02X}")


if __name__ == "__main__":
    import adxl355  # noqa: F811 — needed for Range/PowerMode enums

    main()
