//! Integration tests for 20-bit raw data decoding.

use adxl355::{decode_raw20, raw_to_g, Range};

#[test]
fn test_decode_zero() {
    assert_eq!(decode_raw20(0, 0, 0), 0);
}

#[test]
fn test_decode_positive_max() {
    assert_eq!(decode_raw20(127, 255, 240), 524287);
}

#[test]
fn test_decode_negative_min() {
    assert_eq!(decode_raw20(128, 0, 0), -524288);
}

#[test]
fn test_decode_negative_one() {
    assert_eq!(decode_raw20(255, 255, 240), -1);
}

#[test]
fn test_g_conversion() {
    let g = raw_to_g(524287, Range::G2);
    let expected = 524287.0 * 0.0000039;
    assert!((g - expected).abs() < 1e-6);
}
