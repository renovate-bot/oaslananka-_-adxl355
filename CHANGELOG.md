# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - Unreleased

### Added

- Initial C driver with full API (init, probe, reset, range, power mode, raw/g/mps² read, temperature)
- Mock bus C test infrastructure with register map simulation
- C CMake build system with test/example options
- Python package with type-safe API and mock transport
- Python pytest test suite for register decode, raw conversion, and device flows
- Shared register specification in YAML
- Shared test vectors (JSON) for 20-bit raw decode across all languages
- Rust crate skeleton with raw decode and conversion functions
- Node.js/TypeScript package skeleton with ES module support
- Go module skeleton with interface-based transport abstraction
- C++ RAII wrapper skeleton on top of C core
- Architecture, register map, testing, calibration, and publishing docs
- Root project metadata (README, LICENSE, CHANGELOG, CONTRIBUTING, SECURITY, CODE_OF_CONDUCT)
- Pre-commit configuration with formatting hooks
- .editorconfig and .clang-format for consistent style
