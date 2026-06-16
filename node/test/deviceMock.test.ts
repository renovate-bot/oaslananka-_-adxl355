import { describe, it, expect } from "vitest";
import { ADXL355 } from "../src/device.js";
import { Range, PowerMode, Reg } from "../src/registers.js";
import { Transport } from "../src/transport.js";

class MockTransport implements Transport {
  private regs: Uint8Array;
  callCount = 0;
  calls: Array<{ isWrite: boolean; reg: number }> = [];

  constructor() {
    this.regs = new Uint8Array(128);
    // Set identity registers for probe to succeed
    this.regs[Reg.DEVID_AD] = 0xad;
    this.regs[Reg.DEVID_MST] = 0x1d;
    this.regs[Reg.PARTID] = 0xed;
  }

  setRawXYZ(x: number, y: number, z: number) {
    const encode = (v: number, base: number) => {
      const uv = v & 0xfffff;
      this.regs[base] = (uv >> 12) & 0xff;
      this.regs[base + 1] = (uv >> 4) & 0xff;
      this.regs[base + 2] = (uv & 0x0f) << 4;
    };
    encode(x, Reg.XDATA3);
    encode(y, Reg.YDATA3);
    encode(z, Reg.ZDATA3);
  }

  async readRegister(reg: number, length: number): Promise<Uint8Array> {
    this.calls.push({ isWrite: false, reg });
    this.callCount++;
    return this.regs.slice(reg, reg + length);
  }

  async writeRegister(reg: number, data: Uint8Array): Promise<void> {
    this.calls.push({ isWrite: true, reg });
    this.callCount++;
    this.regs.set(data, reg);
  }

  async delayMs(_ms: number): Promise<void> {
    // no-op
  }
}

describe("ADXL355", () => {
  it("should probe successfully", async () => {
    const transport = new MockTransport();
    const dev = new ADXL355(transport);
    const result = await dev.probe();
    expect(result).toBe(true);
  });

  it("should read raw data", async () => {
    const transport = new MockTransport();
    transport.setRawXYZ(100, -200, 300);
    const dev = new ADXL355(transport);
    await dev.probe();
    const raw = await dev.readRaw();
    expect(raw.x).toBe(100);
    expect(raw.y).toBe(-200);
    expect(raw.z).toBe(300);
  });

  it("should set range", async () => {
    const transport = new MockTransport();
    const dev = new ADXL355(transport);
    await dev.probe();
    await dev.setRange(Range.G8);
    const range = await dev.getRange();
    expect(range).toBe(Range.G8);
  });

  it("should set power mode", async () => {
    const transport = new MockTransport();
    const dev = new ADXL355(transport);
    await dev.probe();
    await dev.setPowerMode(PowerMode.Measurement);
    await dev.setPowerMode(PowerMode.Standby);
  });

  it("should read acceleration in g", async () => {
    const transport = new MockTransport();
    transport.setRawXYZ(524287, 0, -524288);
    const dev = new ADXL355(transport);
    await dev.probe();
    const accel = await dev.readAccelerationG();
    expect(accel.x).toBeGreaterThan(0);
    expect(accel.y).toBe(0);
    expect(accel.z).toBeLessThan(0);
  });

  it("should read temperature raw nominal", async () => {
    const transport = new MockTransport();
    transport["regs"][Reg.TEMP2] = 0x07;
    transport["regs"][Reg.TEMP1] = 0x5d;
    const dev = new ADXL355(transport);
    const raw = await dev.readTemperatureRaw();
    expect(raw).toBe(1885);
  });

  it("should read temperature celsius nominal", async () => {
    const transport = new MockTransport();
    transport["regs"][Reg.TEMP2] = 0x07;
    transport["regs"][Reg.TEMP1] = 0x5d;
    const dev = new ADXL355(transport);
    const temp = await dev.readTemperatureC();
    expect(temp).toBeCloseTo(25.0, 1);
  });

  it("should read temperature celsius 50C", async () => {
    const transport = new MockTransport();
    transport["regs"][Reg.TEMP2] = 0x06;
    transport["regs"][Reg.TEMP1] = 0x7b;
    const dev = new ADXL355(transport);
    const temp = await dev.readTemperatureC();
    expect(temp).toBeCloseTo(50.0, 1);
  });

  it("should read status all clear", async () => {
    const transport = new MockTransport();
    transport["regs"][Reg.STATUS] = 0x00;
    const dev = new ADXL355(transport);
    const status = await dev.readStatus();
    expect(status).toBe(0);
  });

  it("should read status data ready", async () => {
    const transport = new MockTransport();
    transport["regs"][Reg.STATUS] = 0x01;
    const dev = new ADXL355(transport);
    const status = await dev.readStatus();
    expect(status).toBe(1);
  });

  it("should read status fifo full", async () => {
    const transport = new MockTransport();
    transport["regs"][Reg.STATUS] = 0x02;
    const dev = new ADXL355(transport);
    const status = await dev.readStatus();
    expect(status).toBe(2);
  });

  it("should filter default odr", async () => {
    const transport = new MockTransport();
    const dev = new ADXL355(transport);
    const regs = transport["regs"];
    expect(regs[Reg.FILTER] & 0x0f).toBe(0x00);
    expect(regs[Reg.FILTER] & 0x70).toBe(0x00);
  });

  it("should reset call log", async () => {
    const transport = new MockTransport();
    const dev = new ADXL355(transport);
    await dev.reset();
    expect(transport.callCount).toBeGreaterThanOrEqual(1);
    expect(transport.calls[0].isWrite).toBe(true);
    expect(transport.calls[0].reg).toBe(Reg.RESET);
  });

  it("should decode half-scale via read", async () => {
    const transport = new MockTransport();
    transport.setRawXYZ(262144, 0, 0);
    const dev = new ADXL355(transport);
    await dev.probe();
    const raw = await dev.readRaw();
    expect(raw.x).toBe(262144);
  });
});
