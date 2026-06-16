package adxl355

import "errors"

var (
	ErrBus           = errors.New("bus communication error")
	ErrBadDevice     = errors.New("bad device (ID mismatch)")
	ErrInvalidArg    = errors.New("invalid argument")
	ErrNotReady      = errors.New("data not ready")
	ErrTimeout       = errors.New("timeout")
	ErrUnsupported   = errors.New("unsupported operation")
)
