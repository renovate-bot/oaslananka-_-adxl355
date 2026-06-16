/** Base error class for ADXL355 errors. */
export class ADXL355Error extends Error {
  constructor(message: string) {
    super(message);
    this.name = "ADXL355Error";
  }
}

/** Bus communication error. */
export class BusError extends ADXL355Error {
  constructor(message = "Bus communication error") {
    super(message);
    this.name = "BusError";
  }
}

/** Device probe failed. */
export class DeviceNotFoundError extends ADXL355Error {
  constructor(message = "Device not found (ID mismatch)") {
    super(message);
    this.name = "DeviceNotFoundError";
  }
}

/** Invalid configuration argument. */
export class InvalidConfigurationError extends ADXL355Error {
  constructor(message = "Invalid configuration") {
    super(message);
    this.name = "InvalidConfigurationError";
  }
}

/** Data not yet available. */
export class DataNotReadyError extends ADXL355Error {
  constructor(message = "Data not ready") {
    super(message);
    this.name = "DataNotReadyError";
  }
}
