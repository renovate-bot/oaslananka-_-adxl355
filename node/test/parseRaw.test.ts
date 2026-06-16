import { describe, it, expect } from "vitest";
import { decodeRaw20, rawToG, rawToMps2 } from "../src/device.js";
import { Range } from "../src/registers.js";

describe("decodeRaw20", () => {
  it("should decode zero", () => {
    expect(decodeRaw20(0, 0, 0)).toBe(0);
  });

  it("should decode positive one", () => {
    expect(decodeRaw20(0, 0, 16)).toBe(1);
  });

  it("should decode positive max", () => {
    expect(decodeRaw20(127, 255, 240)).toBe(524287);
  });

  it("should decode negative min", () => {
    expect(decodeRaw20(128, 0, 0)).toBe(-524288);
  });

  it("should decode negative one", () => {
    expect(decodeRaw20(255, 255, 240)).toBe(-1);
  });

  it("should decode half-scale positive", () => {
    expect(decodeRaw20(64, 0, 0)).toBe(262144);
  });

  it("should decode half-scale negative", () => {
    expect(decodeRaw20(192, 0, 0)).toBe(-262144);
  });
});

describe("rawToG", () => {
  it("should return 0 for zero raw", () => {
    expect(rawToG(0, Range.G2)).toBeCloseTo(0);
  });

  it("should convert positive max at 2g", () => {
    const expected = 524287 * 0.0000039;
    expect(rawToG(524287, Range.G2)).toBeCloseTo(expected, 6);
  });
});

describe("rawToMps2", () => {
  it("should convert to m/s²", () => {
    const expected = 100000 * 0.0000039 * 9.80665;
    expect(rawToMps2(100000, Range.G2)).toBeCloseTo(expected, 5);
  });
});
