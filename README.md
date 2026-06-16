# ADXL355

Cross-platform ADXL355 accelerometer driver for C, C++, Python, Rust, Node.js and Go.

Transport-agnostic, testable, production-ready driver family with shared register specification and consistent API across all languages.

## Status

| Language | Package | Status |
|---|---|---|
| C | CMake library | ✅ MVP |
| C++ | C++17 wrapper | ✅ MVP |
| Python | PyPI package | ✅ MVP |
| Rust | crates.io crate | ✅ MVP |
| Node.js | npm package | ✅ MVP |
| Go | Go module | ✅ MVP |

## Features

- Transport-agnostic design (SPI/I2C abstraction via bus interface)
- C core reference implementation
- Python package with type hints
- Rust, Node.js, Go and C++ packages with shared API design
- Mock transport testing (no hardware required)
- Raw 20-bit acceleration decoding with golden test vectors
- Range-based g and m/s² conversion
- Temperature sensor readout
- FIFO basic support
- Self-test and offset calibration API
- Register map specification and documentation

## Quick Start

### Python

```bash
cd python
pip install -e .
python examples/basic_read.py
```

### C

```bash
cmake -S c -B c/build -DADXL355_BUILD_TESTS=ON -DADXL355_BUILD_EXAMPLES=ON
cmake --build c/build
ctest --test-dir c/build --output-on-failure
./c/build/examples/basic_read
```

### Rust

```bash
cd rust
cargo test
cargo run --example basic
```

### Node.js

```bash
cd node
npm install
npm test
```

### Go

```bash
cd go
go test ./...
```

### C++

```bash
cmake -S cpp -B cpp/build -DADXL355_BUILD_TESTS=ON
cmake --build cpp/build
ctest --test-dir cpp/build --output-on-failure
```

## Architecture

See [docs/architecture.md](docs/architecture.md) for detailed architecture documentation.

## Testing

See [docs/testing.md](docs/testing.md) for testing methodology.

## License

MIT
