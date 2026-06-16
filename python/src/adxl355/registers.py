"""
ADXL355 register addresses, enums, and bit masks.

Preliminary values - verify against official ADXL355 datasheet.
"""

from enum import IntEnum


class Register(IntEnum):
    """ADXL355 register addresses."""

    DEVID_AD = 0x00
    DEVID_MST = 0x01
    PARTID = 0x02
    REVID = 0x03
    STATUS = 0x04
    FIFO_ENTRIES = 0x05
    TEMP2 = 0x06
    TEMP1 = 0x07
    XDATA3 = 0x08
    XDATA2 = 0x09
    XDATA1 = 0x0A
    YDATA3 = 0x0B
    YDATA2 = 0x0C
    YDATA1 = 0x0D
    ZDATA3 = 0x0E
    ZDATA2 = 0x0F
    ZDATA1 = 0x10
    FIFO_DATA = 0x11
    OFFSET_X_H = 0x1E
    OFFSET_X_L = 0x1F
    OFFSET_Y_H = 0x20
    OFFSET_Y_L = 0x21
    OFFSET_Z_H = 0x22
    OFFSET_Z_L = 0x23
    ACT_EN = 0x24
    ACT_THRESH_H = 0x25
    ACT_THRESH_L = 0x26
    ACT_COUNT = 0x27
    FILTER = 0x28
    FIFO_SAMPLES = 0x29
    INT_MAP = 0x2A
    SYNC = 0x2B
    RANGE = 0x2C
    POWER_CTL = 0x2D
    SELF_TEST = 0x2E
    RESET = 0x2F


class Range(IntEnum):
    """Acceleration range selection."""

    G2 = 0
    G4 = 1
    G8 = 2


class PowerMode(IntEnum):
    """Power mode control."""

    STANDBY = 0
    MEASUREMENT = 1


class ODR(IntEnum):
    """Output data rate selection."""

    HZ_4000 = 0
    HZ_2000 = 1
    HZ_1000 = 2
    HZ_500 = 3
    HZ_250 = 4
    HZ_125 = 5
    HZ_62_5 = 6
    HZ_31_25 = 7
    HZ_15_625 = 8
    HZ_7_813 = 9
    HZ_3_906 = 10


# Status register bits
STATUS_NVM_BUSY = 1 << 7
STATUS_ACTIVITY = 1 << 6
STATUS_FIFO_OVR = 1 << 5
STATUS_FIFO_FULL = 1 << 4
STATUS_DATA_RDY = 1 << 3

# Filter register masks
FILTER_ODR_MASK = 0xF0
FILTER_ODR_SHIFT = 4
FILTER_LPF_MASK = 0x0F

# Range register mask
RANGE_SEL_MASK = 0x03
