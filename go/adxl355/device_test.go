package adxl355

import (
	"testing"
)

// mockTransport implements Transport for testing.
type mockTransport struct {
	regs [128]byte
}

func newMockTransport() *mockTransport {
	m := &mockTransport{}
	m.regs[RegDEVID_AD] = DEVID_AD_VALUE
	m.regs[RegDEVID_MST] = DEVID_MST_VALUE
	m.regs[RegPARTID] = PARTID_VALUE
	return m
}

func (m *mockTransport) ReadRegister(reg byte, length int) ([]byte, error) {
	return m.regs[reg : reg+byte(length)], nil
}

func (m *mockTransport) WriteRegister(reg byte, data []byte) error {
	copy(m.regs[reg:], data)
	return nil
}

func (m *mockTransport) DelayMs(ms uint32) {}

func (m *mockTransport) setRawXYZ(x, y, z int32) {
	encode := func(v int32, base byte) {
		uv := uint32(v) & 0xFFFFF
		m.regs[base] = byte((uv >> 12) & 0xFF)
		m.regs[base+1] = byte((uv >> 4) & 0xFF)
		m.regs[base+2] = byte((uv & 0x0F) << 4)
	}
	encode(x, RegXDATA3)
	encode(y, RegYDATA3)
	encode(z, RegZDATA3)
}

func TestDecodeRaw20(t *testing.T) {
	tests := []struct {
		b0, b1, b2 byte
		expected   int32
	}{
		{0, 0, 0, 0},
		{0, 0, 16, 1},
		{127, 255, 240, 524287},
		{128, 0, 0, -524288},
		{255, 255, 240, -1},
	}

	for _, tt := range tests {
		result := DecodeRaw20(tt.b0, tt.b1, tt.b2)
		if result != tt.expected {
			t.Errorf("DecodeRaw20(%d,%d,%d) = %d, want %d",
				tt.b0, tt.b1, tt.b2, result, tt.expected)
		}
	}
}

func TestRawToG(t *testing.T) {
	g := RawToG(524287, Range2G)
	expected := float32(524287) * Scale2GGPerLSB
	if g != expected {
		t.Errorf("RawToG = %f, want %f", g, expected)
	}
}

func TestRawToMps2(t *testing.T) {
	v := RawToMps2(100000, Range2G)
	expected := float32(100000) * Scale2GGPerLSB * StandardGravityMS2
	if v != expected {
		t.Errorf("RawToMps2 = %f, want %f", v, expected)
	}
}

func TestProbe(t *testing.T) {
	mock := newMockTransport()
	dev := New(mock)
	ok, err := dev.Probe()
	if err != nil {
		t.Fatalf("Probe failed: %v", err)
	}
	if !ok {
		t.Fatal("Probe returned false")
	}
}

func TestSetRange(t *testing.T) {
	mock := newMockTransport()
	dev := New(mock)
	dev.Probe()

	if err := dev.SetRange(Range8G); err != nil {
		t.Fatalf("SetRange failed: %v", err)
	}

	r, err := dev.GetRange()
	if err != nil {
		t.Fatalf("GetRange failed: %v", err)
	}
	if r != Range8G {
		t.Fatalf("Range = %d, want %d", r, Range8G)
	}
}

func TestReadRaw(t *testing.T) {
	mock := newMockTransport()
	mock.setRawXYZ(100, -200, 300)
	dev := New(mock)
	dev.Probe()

	raw, err := dev.ReadRaw()
	if err != nil {
		t.Fatalf("ReadRaw failed: %v", err)
	}
	if raw.X != 100 || raw.Y != -200 || raw.Z != 300 {
		t.Fatalf("Raw = %+v, want {X:100 Y:-200 Z:300}", raw)
	}
}
