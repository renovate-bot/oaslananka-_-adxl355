/**
 * Transport abstraction for ADXL355 communication.
 * Implementations wrap SPI, I2C, or mock backends.
 */
export interface Transport {
  /** Read `length` bytes starting at register `reg`. */
  readRegister(reg: number, length: number): Promise<Uint8Array>;
  /** Write `data` bytes starting at register `reg`. */
  writeRegister(reg: number, data: Uint8Array): Promise<void>;
  /** Blocking delay in milliseconds (optional). */
  delayMs?(ms: number): Promise<void>;
}
