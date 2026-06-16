/// Integration tests for ADXL355 device with mock transport.

use adxl355::{Adxl355, PowerMode, Error};
use adxl355::registers;

struct MockBus {
    regs: [u8; 128],
}

impl MockBus {
    fn new() -> Self {
        let mut bus = MockBus { regs: [0; 128] };
        bus.regs[registers::reg::DEVID_AD as usize] = registers::id::DEVID_AD;
        bus.regs[registers::reg::DEVID_MST as usize] = registers::id::DEVID_MST;
        bus.regs[registers::reg::PARTID as usize] = registers::id::PARTID;
        bus
    }
}

impl adxl355::device::Transport for MockBus {
    fn read_register(&mut self, reg: u8, len: u8) -> Result<Vec<u8>, Error> {
        let start = reg as usize;
        let end = start + len as usize;
        Ok(self.regs[start..end].to_vec())
    }

    fn write_register(&mut self, reg: u8, data: &[u8]) -> Result<(), Error> {
        let start = reg as usize;
        for (i, &b) in data.iter().enumerate() {
            if start + i < self.regs.len() {
                self.regs[start + i] = b;
            }
        }
        Ok(())
    }

    fn delay_ms(&mut self, _ms: u32) {}
}

#[test]
fn test_probe_ok() {
    let bus = MockBus::new();
    let mut dev = Adxl355::new(bus);
    assert!(dev.probe().is_ok());
}

#[test]
fn test_set_power_mode() {
    let bus = MockBus::new();
    let mut dev = Adxl355::new(bus);
    dev.probe().unwrap();
    assert!(dev.set_power_mode(PowerMode::Measurement).is_ok());
    assert!(dev.set_power_mode(PowerMode::Standby).is_ok());
}

#[test]
fn test_reset() {
    let bus = MockBus::new();
    let mut dev = Adxl355::new(bus);
    assert!(dev.reset().is_ok());
}
