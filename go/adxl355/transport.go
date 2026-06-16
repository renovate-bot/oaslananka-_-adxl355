package adxl355

// Transport is the abstract bus interface for ADXL355 communication.
type Transport interface {
	// ReadRegister reads len bytes starting at register reg.
	ReadRegister(reg byte, length int) ([]byte, error)
	// WriteRegister writes data bytes starting at register reg.
	WriteRegister(reg byte, data []byte) error
	// DelayMs blocks for ms milliseconds.
	DelayMs(ms uint32)
}
