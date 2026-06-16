/**
 * ADXL355 register addresses and constants.
 * Preliminary — verify against official ADXL355 datasheet.
 */

/** Register addresses */
export const enum Reg {
  DEVID_AD = 0x00,
  DEVID_MST = 0x01,
  PARTID = 0x02,
  REVID = 0x03,
  STATUS = 0x04,
  FIFO_ENTRIES = 0x05,
  TEMP2 = 0x06,
  TEMP1 = 0x07,
  XDATA3 = 0x08,
  XDATA2 = 0x09,
  XDATA1 = 0x0a,
  YDATA3 = 0x0b,
  YDATA2 = 0x0c,
  YDATA1 = 0x0d,
  ZDATA3 = 0x0e,
  ZDATA2 = 0x0f,
  ZDATA1 = 0x10,
  FIFO_DATA = 0x11,
  OFFSET_X_H = 0x1e,
  OFFSET_X_L = 0x1f,
  OFFSET_Y_H = 0x20,
  OFFSET_Y_L = 0x21,
  OFFSET_Z_H = 0x22,
  OFFSET_Z_L = 0x23,
  ACT_EN = 0x24,
  ACT_THRESH_H = 0x25,
  ACT_THRESH_L = 0x26,
  ACT_COUNT = 0x27,
  FILTER = 0x28,
  FIFO_SAMPLES = 0x29,
  INT_MAP = 0x2a,
  SYNC = 0x2b,
  RANGE = 0x2c,
  POWER_CTL = 0x2d,
  SELF_TEST = 0x2e,
  RESET = 0x2f,
}

/** Expected device identity values */
export const DEVID_AD_VALUE = 0xad;
export const DEVID_MST_VALUE = 0x1d;
export const PARTID_VALUE = 0xed;

/** Software reset code */
export const RESET_CODE = 0x52;

/** Acceleration range */
export enum Range {
  G2 = 0,
  G4 = 1,
  G8 = 2,
}

/** Power mode */
export enum PowerMode {
  Standby = 0,
  Measurement = 1,
}

/** Output data rate */
export enum Odr {
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

/** Scaling constants (g per LSB) */
export const SCALE_2G_G_PER_LSB = 0.0000039;
export const SCALE_4G_G_PER_LSB = 0.0000078;
export const SCALE_8G_G_PER_LSB = 0.0000156;

/** Standard gravity (m/s²) */
export const STANDARD_GRAVITY_M_S2 = 9.80665;
