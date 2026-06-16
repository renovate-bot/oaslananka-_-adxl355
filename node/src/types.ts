/** Raw 20-bit acceleration data (sign-extended to number). */
export interface RawXYZ {
  x: number;
  y: number;
  z: number;
}

/** Acceleration in floating-point units. */
export interface AccelXYZ {
  x: number;
  y: number;
  z: number;
}
