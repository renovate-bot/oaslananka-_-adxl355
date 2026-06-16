package adxl355

// Register addresses for the ADXL355.
// Preliminary — verify against official ADXL355 datasheet.
const (
	RegDEVID_AD     = 0x00
	RegDEVID_MST    = 0x01
	RegPARTID       = 0x02
	RegREVID        = 0x03
	RegSTATUS       = 0x04
	RegFIFO_ENTRIES = 0x05
	RegTEMP2        = 0x06
	RegTEMP1        = 0x07
	RegXDATA3       = 0x08
	RegXDATA2       = 0x09
	RegXDATA1       = 0x0A
	RegYDATA3       = 0x0B
	RegYDATA2       = 0x0C
	RegYDATA1       = 0x0D
	RegZDATA3       = 0x0E
	RegZDATA2       = 0x0F
	RegZDATA1       = 0x10
	RegFIFO_DATA    = 0x11
	RegOFFSET_X_H   = 0x1E
	RegOFFSET_X_L   = 0x1F
	RegOFFSET_Y_H   = 0x20
	RegOFFSET_Y_L   = 0x21
	RegOFFSET_Z_H   = 0x22
	RegOFFSET_Z_L   = 0x23
	RegACT_EN       = 0x24
	RegACT_THRESH_H = 0x25
	RegACT_THRESH_L = 0x26
	RegACT_COUNT    = 0x27
	RegFILTER       = 0x28
	RegFIFO_SAMPLES = 0x29
	RegINT_MAP      = 0x2A
	RegSYNC         = 0x2B
	RegRANGE        = 0x2C
	RegPOWER_CTL    = 0x2D
	RegSELF_TEST    = 0x2E
	RegRESET        = 0x2F
)

// Expected identity register values.
const (
	DEVID_AD_VALUE  = 0xAD
	DEVID_MST_VALUE = 0x1D
	PARTID_VALUE    = 0xED
)

// Reset code.
const RESET_CODE = 0x52

// Acceleration range.
type Range int

const (
	Range2G Range = 0
	Range4G Range = 1
	Range8G Range = 2
)

// Scale factors (g per LSB).
const (
	Scale2GGPerLSB = 0.0000039
	Scale4GGPerLSB = 0.0000078
	Scale8GGPerLSB = 0.0000156
)

// Standard gravity in m/s².
const StandardGravityMS2 = 9.80665

// Power mode.
type PowerMode int

const (
	PowerStandby    PowerMode = 0
	PowerMeasurement PowerMode = 1
)

// Output data rate.
type ODR int

const (
	ODR4000Hz  ODR = 0
	ODR2000Hz  ODR = 1
	ODR1000Hz  ODR = 2
	ODR500Hz   ODR = 3
	ODR250Hz   ODR = 4
	ODR125Hz   ODR = 5
	ODR62_5Hz  ODR = 6
	ODR31_25Hz ODR = 7
	ODR15_625Hz ODR = 8
	ODR7_813Hz ODR = 9
	ODR3_906Hz ODR = 10
)
