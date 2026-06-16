"""ADXL355 calibration example using mock transport.

Measures offset by averaging N samples at rest,
then computes the offset register values.
"""

from adxl355 import ADXL355, MockTransport, Range


def measure_offsets(dev: ADXL355, samples: int = 100):
    """Average `samples` raw readings per axis."""
    sx = sy = sz = 0
    for _ in range(samples):
        raw = dev.read_raw()
        sx += raw.x
        sy += raw.y
        sz += raw.z
    n = float(samples)
    return (sx / n, sy / n, sz / n)


def main() -> None:
    transport = MockTransport()
    dev = ADXL355(transport)

    if not dev.probe():
        print("ERROR: Device not found")
        return

    dev.set_range(Range.G4)
    dev.set_power_mode(adxl355.PowerMode.MEASUREMENT)

    ox, oy, oz = measure_offsets(dev)

    # At 4g range, scale = 7.8 µg/LSB
    scale_g = 7.8e-6
    print(f"Offsets (raw LSB):  x={ox:.1f}  y={oy:.1f}  z={oz:.1f}")
    print(f"Offsets (g):        x={ox * scale_g:.6f}  y={oy * scale_g:.6f}  z={oz * scale_g:.6f}")
    print("(Mock data — real hardware will show actual offsets)")


if __name__ == "__main__":
    import adxl355  # noqa — enums

    main()
