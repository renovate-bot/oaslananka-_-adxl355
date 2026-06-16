# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in this library, please report it privately.

**Do not** open a public GitHub issue. Instead, contact the maintainer directly.

We will acknowledge receipt within 48 hours and provide a timeline for a fix.

## Scope

- Public API input validation
- Buffer overflow protection (C core)
- Sign extension correctness
- Integer overflow handling
- Data integrity of sensor readings

## Out of Scope

- Physical access attacks on the sensor or bus
- Side-channel attacks requiring instrumentation
- Denial of service via excessive SPI/I2C traffic
