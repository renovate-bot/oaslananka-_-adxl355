package adxl355

import "testing"

func TestDecodeZero(t *testing.T) {
	if DecodeRaw20(0, 0, 0) != 0 {
		t.Fail()
	}
}

func TestDecodePositiveMax(t *testing.T) {
	if DecodeRaw20(127, 255, 240) != 524287 {
		t.Fail()
	}
}

func TestDecodeNegativeMin(t *testing.T) {
	if DecodeRaw20(128, 0, 0) != -524288 {
		t.Fail()
	}
}

func TestDecodeNegativeOne(t *testing.T) {
	if DecodeRaw20(255, 255, 240) != -1 {
		t.Fail()
	}
}

func TestDecodeHalfScalePositive(t *testing.T) {
	if DecodeRaw20(64, 0, 0) != 262144 {
		t.Fail()
	}
}

func TestDecodeHalfScaleNegative(t *testing.T) {
	if DecodeRaw20(192, 0, 0) != -262144 {
		t.Fail()
	}
}
