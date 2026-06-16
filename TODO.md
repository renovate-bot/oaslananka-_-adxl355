# TODO

## Pre-v0.1.0 Release

### General
- [ ] Verify register addresses and bit fields against official ADXL355 datasheet
- [ ] Confirm temperature conversion formula from datasheet
- [ ] Verify scale factors (µg/LSB) from datasheet
- [ ] Confirm SPI read/write command format
- [ ] Confirm I2C 7-bit address options
- [ ] Add CI configuration (GitHub Actions)
- [x] Fix copyright holder name in LICENSE

### C
- [ ] FIFO read API implementation
- [ ] Interrupt configuration API
- [ ] Self-test API hardware testing
- [ ] Continuous data acquisition example
- [ ] Verify CMake builds on Linux/GCC, ARM GCC, MinGW
- [ ] Add doxygen-style documentation comments to public headers
- [x] Core MVP (probe, read_raw, set_range, power modes, temperature, reset)
- [x] Mock bus testing (17 tests passing)

### Python
- [ ] spidev adapter implementation
- [ ] smbus2 adapter implementation
- [ ] Calibration helper utilities
- [ ] FIFO read support
- [ ] Hardware-in-the-loop test examples
- [ ] Verify ruff and mypy compliance
- [ ] Add more device-level integration tests
- [x] Core MVP (full Device class, 39 tests passing)

### Rust
- [ ] embedded-hal trait integration
- [ ] no_std support verification
- [ ] More comprehensive error types
- [x] Full device API (probe, set_range, read_raw, power modes, temperature, reset)
- [x] Mock transport with tests (20 tests passing)

### Node.js
- [ ] spi-device adapter
- [ ] i2c-bus adapter
- [ ] npm package.json publish configuration
- [x] Full device API (13 tests passing)

### Go
- [ ] spidev/Linux implementation
- [ ] Example with real hardware
- [x] Full device API (all tests passing)

### C++
- [ ] Arduino/PlatformIO compatibility layer
- [ ] Exception-free error handling option
- [x] Full RAII device class with all C API methods (3 tests passing)

### Documentation
- [ ] Hardware wiring diagrams
- [ ] Raspberry Pi setup guide
- [ ] Hardware test plan with steps
- [ ] Interrupt and FIFO detailed documentation
- [ ] API reference docs for each language
- [ ] Video/images for hardware setup
- [x] Architecture documentation
- [x] Register map documentation
- [x] Testing guide
- [x] Calibration guide
- [x] Publishing guide

### Testing
- [ ] Cross-language test vector verification (all languages produce same decode results)
- [ ] Hardware-in-the-loop test procedure
- [ ] Continuous integration with hardware test runner
