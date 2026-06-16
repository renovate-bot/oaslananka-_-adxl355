package adxl355

// RawXYZ holds raw 20-bit acceleration data (sign-extended).
type RawXYZ struct {
	X int32
	Y int32
	Z int32
}

// AccelXYZ holds acceleration in floating-point units.
type AccelXYZ struct {
	X float32
	Y float32
	Z float32
}
