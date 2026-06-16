"""
ADXL355 scaling constants.

All values are preliminary and should be verified against the official
ADXL355 datasheet.
"""

# Scale factors (g per LSB) for each range setting
# TODO: Verify against official ADXL355 datasheet
SCALE_2G_G_PER_LSB: float = 0.0000039
SCALE_4G_G_PER_LSB: float = 0.0000078
SCALE_8G_G_PER_LSB: float = 0.0000156

# Standard gravity (m/s²)
STANDARD_GRAVITY_M_S2: float = 9.80665

# Expected identity register values
DEVID_AD: int = 0xAD
DEVID_MST: int = 0x1D
PARTID: int = 0xED

# Software reset code
RESET_CODE: int = 0x52
