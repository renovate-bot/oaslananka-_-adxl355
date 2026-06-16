//! ADXL355 register addresses and bit masks.
//!
//! Preliminary values — verify against official ADXL355 datasheet.

/// Register addresses.
#[allow(non_snake_case, non_upper_case_globals)]
pub mod reg {
    /// Device ID (Analog Devices).
    pub const DEVID_AD: u8 = 0x00;
    /// MEMS sensor ID.
    pub const DEVID_MST: u8 = 0x01;
    /// Part ID.
    pub const PARTID: u8 = 0x02;
    /// Revision ID.
    pub const REVID: u8 = 0x03;
    /// Status register.
    pub const STATUS: u8 = 0x04;
    /// FIFO entry count.
    pub const FIFO_ENTRIES: u8 = 0x05;
    /// Temperature high byte.
    pub const TEMP2: u8 = 0x06;
    /// Temperature low byte.
    pub const TEMP1: u8 = 0x07;
    /// X-axis acceleration MSB.
    pub const XDATA3: u8 = 0x08;
    /// X-axis acceleration mid byte.
    pub const XDATA2: u8 = 0x09;
    /// X-axis acceleration LSB.
    pub const XDATA1: u8 = 0x0A;
    /// Y-axis acceleration MSB.
    pub const YDATA3: u8 = 0x0B;
    /// Y-axis acceleration mid byte.
    pub const YDATA2: u8 = 0x0C;
    /// Y-axis acceleration LSB.
    pub const YDATA1: u8 = 0x0D;
    /// Z-axis acceleration MSB.
    pub const ZDATA3: u8 = 0x0E;
    /// Z-axis acceleration mid byte.
    pub const ZDATA2: u8 = 0x0F;
    /// Z-axis acceleration LSB.
    pub const ZDATA1: u8 = 0x10;
    /// FIFO data read.
    pub const FIFO_DATA: u8 = 0x11;
    /// X-axis offset high byte.
    pub const OFFSET_X_H: u8 = 0x1E;
    /// X-axis offset low byte.
    pub const OFFSET_X_L: u8 = 0x1F;
    /// Y-axis offset high byte.
    pub const OFFSET_Y_H: u8 = 0x20;
    /// Y-axis offset low byte.
    pub const OFFSET_Y_L: u8 = 0x21;
    /// Z-axis offset high byte.
    pub const OFFSET_Z_H: u8 = 0x22;
    /// Z-axis offset low byte.
    pub const OFFSET_Z_L: u8 = 0x23;
    /// Activity detection enable.
    pub const ACT_EN: u8 = 0x24;
    /// Activity threshold high byte.
    pub const ACT_THRESH_H: u8 = 0x25;
    /// Activity threshold low byte.
    pub const ACT_THRESH_L: u8 = 0x26;
    /// Activity count.
    pub const ACT_COUNT: u8 = 0x27;
    /// Filter / output data rate control.
    pub const FILTER: u8 = 0x28;
    /// FIFO sample count threshold.
    pub const FIFO_SAMPLES: u8 = 0x29;
    /// Interrupt mapping.
    pub const INT_MAP: u8 = 0x2A;
    /// External synchronization control.
    pub const SYNC: u8 = 0x2B;
    /// Acceleration range selection.
    pub const RANGE: u8 = 0x2C;
    /// Power control.
    pub const POWER_CTL: u8 = 0x2D;
    /// Self-test control.
    pub const SELF_TEST: u8 = 0x2E;
    /// Software reset (write 0x52).
    pub const RESET: u8 = 0x2F;
}

/// Expected device identity values.
pub mod id {
    pub const DEVID_AD: u8 = 0xAD;
    pub const DEVID_MST: u8 = 0x1D;
    pub const PARTID: u8 = 0xED;
}

/// Software reset code.
pub const RESET_CODE: u8 = 0x52;

/// Power mode bit.
pub const POWER_MODE_BIT: u8 = 0;

/// Acceleration range selection.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Range {
    G2 = 0,
    G4 = 1,
    G8 = 2,
}

impl Range {
    /// Convert to register value.
    pub fn to_register(self) -> u8 {
        self as u8
    }

    /// Create from register value.
    pub fn from_register(val: u8) -> Option<Self> {
        match val & 0x03 {
            0 => Some(Range::G2),
            1 => Some(Range::G4),
            2 => Some(Range::G8),
            _ => None,
        }
    }

    /// Scale factor in g per LSB.
    pub fn scale_g_per_lsb(self) -> f32 {
        match self {
            Range::G2 => 0.0000039,
            Range::G4 => 0.0000078,
            Range::G8 => 0.0000156,
        }
    }
}

/// Power mode.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum PowerMode {
    Standby = 0,
    Measurement = 1,
}

/// Output data rate.
#[derive(Debug, Clone, Copy, PartialEq)]
pub enum Odr {
    Hz4000 = 0,
    Hz2000 = 1,
    Hz1000 = 2,
    Hz500 = 3,
    Hz250 = 4,
    Hz125 = 5,
    Hz62_5 = 6,
    Hz31_25 = 7,
    Hz15_625 = 8,
    Hz7_813 = 9,
    Hz3_906 = 10,
}

/// Standard gravity (m/s²).
pub const STANDARD_GRAVITY_M_S2: f32 = 9.80665;
