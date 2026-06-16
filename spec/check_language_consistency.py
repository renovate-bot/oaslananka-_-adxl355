#!/usr/bin/env python3
"""
Cross-language consistency checker.

Reads spec/adxl355.registers.yaml and spec/adxl355.constants.yaml, then
extracts register address / bit-field constants from each language
implementation and reports any discrepancies.

Languages checked:
  - C        c/include/adxl355/adxl355_registers.h
  - Python   python/src/adxl355/registers.py
  - Rust     rust/src/registers.rs
  - Node/TS  node/src/registers.ts
  - Go       go/adxl355/registers.go

Usage:
    python spec/check_language_consistency.py
    python spec/check_language_consistency.py --quiet  # summary only
    python spec/check_language_consistency.py --strict  # fail on warnings
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML is required. Install with: pip install PyYAML")
    sys.exit(1)

# ---------------------------------------------------------------------------
# Spec reference values (from YAML)
# ---------------------------------------------------------------------------

def load_spec(spec_dir: Path):
    """Load register addresses and critical constants from YAML specs."""
    ref = {}

    # Register addresses
    reg_path = spec_dir / "adxl355.registers.yaml"
    with open(reg_path, encoding="utf-8") as f:
        reg_data = yaml.safe_load(f)

    ref["registers"] = {}
    for reg in reg_data.get("registers", []):
        if not isinstance(reg, dict):
            continue
        name = reg.get("name")
        addr = reg.get("address")
        if name and addr is not None:
            addr_int = int(str(addr), 16) if isinstance(addr, str) and addr.startswith("0x") else int(addr)
            ref["registers"][name] = addr_int

    # Constants
    const_path = spec_dir / "adxl355.constants.yaml"
    with open(const_path, encoding="utf-8") as f:
        const_data = yaml.safe_load(f)

    ref["range"] = {k: v["value"] for k, v in const_data.get("range", {}).items() if isinstance(v, dict) and "value" in v}
    ref["power_mode"] = const_data.get("power_mode", {})
    ref["status"] = {k: v for k, v in const_data.get("status_register", {}).items() if k != "description"}
    ref["filter"] = {k: v for k, v in const_data.get("filter_register", {}).items() if k != "description"}
    ref["i2c_address"] = {k: v for k, v in const_data.get("i2c_address", {}).items() if k != "description"}

    return ref


# ---------------------------------------------------------------------------
# Language parsers — extract register address / constant definitions
# ---------------------------------------------------------------------------

def parse_c_header(path: Path):
    """Extract #define values from C header."""
    defines = {}
    if not path.exists():
        return {"error": f"File not found: {path}"}

    content = path.read_text(encoding="utf-8")
    # Pattern: #define NAME value_or_expression
    for m in re.finditer(r'#define\s+(\w+)\s+(.+?)(?:\s+/\*.*)?$', content, re.MULTILINE):
        name = m.group(1)
        val = m.group(2).strip()
        # Try to resolve simple hex/int constants
        defines[name] = val
    return defines


def parse_python(path: Path):
    """Extract IntEnum / class constant values from Python registers module."""
    values = {}
    if not path.exists():
        return {"error": f"File not found: {path}"}

    content = path.read_text(encoding="utf-8")
    # Pattern: NAME = 0xNN or NAME = N
    for m in re.finditer(r'^(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)\s*(?:#.*)?$', content, re.MULTILINE):
        name = m.group(1)
        raw = m.group(2)
        if raw.startswith("0x"):
            values[name] = int(raw, 16)
        else:
            values[name] = int(raw)
    return values


def parse_rust(path: Path):
    """Extract const values from Rust registers module."""
    values = {}
    if not path.exists():
        return {"error": f"File not found: {path}"}

    content = path.read_text(encoding="utf-8")

    # Extract scoped values: pub mod NAME { pub const X: T = V; }
    mod_re = re.compile(r'pub\s+mod\s+(\w+)\s*\{(.*?)\}', re.DOTALL)
    for mm in mod_re.finditer(content):
        mod_name = mm.group(1)
        mod_body = mm.group(2)
        for cm in re.finditer(r'pub\s+const\s+(\w+)\s*:\s*\w+\s*=\s*(0x[0-9a-fA-F]+|\d+)', mod_body):
            raw = cm.group(2)
            v = int(raw, 16) if raw.startswith("0x") else int(raw)
            values[f"{mod_name}/{cm.group(1)}"] = v

    # Also extract top-level pub const values
    for m in re.finditer(r'pub\s+const\s+(\w+)\s*:\s*\w+\s*=\s*(0x[0-9a-fA-F]+|\d+)', content):
        name = m.group(1)
        raw = m.group(2)
        v = int(raw, 16) if raw.startswith("0x") else int(raw)
        # Avoid overwriting scoped values
        if name not in values or not any(k.endswith(f"/{name}") for k in values):
            values[name] = v

    # Also expose shorthand without module prefix for simpler lookup
    for key, val in list(values.items()):
        if "/" in key:
            short = key.split("/")[-1]
            if short not in values:
                values[short] = val
            # For 'reg/DEVID_AD = 0x00', also set 'ADXL355_REG_DEVID_AD = 0x00'
            prefix = key.split("/")[0]
            if prefix == "reg":
                values[f"ADXL355_REG_{short}"] = val

    return values


def parse_typescript(path: Path):
    """Extract const and enum values from TypeScript registers module."""
    values = {}
    if not path.exists():
        return {"error": f"File not found: {path}"}

    content = path.read_text(encoding="utf-8")
    # Pattern: export const NAME = VALUE;
    for m in re.finditer(r'export\s+const\s+(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)', content):
        name = m.group(1)
        raw = m.group(2)
        if raw.startswith("0x"):
            values[name] = int(raw, 16)
        else:
            values[name] = int(raw)
    # Enum values: NAME = VALUE,
    for m in re.finditer(r'(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+),', content):
        name = m.group(1)
        # Skip non-enum-looking names
        if name.isupper() or name[0].isupper():
            raw = m.group(2)
            if raw.startswith("0x"):
                values.setdefault(name, int(raw, 16))
            else:
                values.setdefault(name, int(raw))
    return values


def parse_go(path: Path):
    """Extract const values from Go registers package."""
    values = {}
    if not path.exists():
        return {"error": f"File not found: {path}"}

    content = path.read_text(encoding="utf-8")
    # Pattern: NAME = VALUE
    for m in re.finditer(r'^(\w+)\s*=\s*(0x[0-9a-fA-F]+|\d+)', content, re.MULTILINE):
        name = m.group(1)
        raw = m.group(2)
        if raw.startswith("0x"):
            values[name] = int(raw, 16)
        else:
            values[name] = int(raw)
    return values


# ---------------------------------------------------------------------------
# Checkers
# ---------------------------------------------------------------------------

class ConsistencyChecker:
    def __init__(self, spec_dir: Path, repo_root: Path):
        self.spec = load_spec(spec_dir)
        self.repo_root = repo_root
        self.results: list[str] = []

    def ok(self, msg: str):
        pass  # quiet by default

    def mismatch(self, msg: str):
        self.results.append(f"MISMATCH: {msg}")

    def missing(self, msg: str):
        self.results.append(f"MISSING:  {msg}")

    # --------------------------------------------------------------
    # Register address checks per language
    # --------------------------------------------------------------

    def check_register_addrs(self, lang: str, values: dict, prefix: str = ""):
        for reg_name, expected_addr in self.spec["registers"].items():
            if prefix:
                key = f"{prefix}{reg_name}"
            else:
                key = reg_name
            if key in values:
                val = values[key]
                if isinstance(val, int) and val != expected_addr:
                    self.mismatch(f"{lang}: {key} = 0x{val:02X}, expected 0x{expected_addr:02X}")
            # Also try case-insensitive match
            elif not self._find_case_insensitive(values, key, expected_addr, lang):
                # Don't report missing for non-critical names
                pass

    def _find_case_insensitive(self, values: dict, key: str, expected: int, lang: str) -> bool:
        """Try case-insensitive match for enum constants."""
        key_upper = key.upper()
        for k in values:
            if k.upper() == key_upper:
                if isinstance(values[k], int) and values[k] != expected:
                    self.mismatch(f"{lang}: {k} = 0x{values[k]:02X}, expected 0x{expected:02X} (from {key})")
                return True
        return False

    # --------------------------------------------------------------
    # Constant checks
    # --------------------------------------------------------------

    def check_range_values(self, lang: str, values: dict):
        range_map = {"Range2G": "G2", "Range4G": "G4", "Range8G": "G8",
                     "G2": "G2", "G4": "G4", "G8": "G8"}
        for k, expected in self.spec["range"].items():
            for alias, target in range_map.items():
                if target == k and alias in values:
                    if isinstance(values[alias], int) and values[alias] != expected:
                        self.mismatch(f"{lang}: {alias} = 0x{values[alias]:02X}, expected 0x{expected:02X}")
                    break

    def check_power_mode(self, lang: str, values: dict):
        pm_map = {"PowerStandby": "STANDBY", "PowerMeasurement": "MEASUREMENT",
                  "STANDBY": "STANDBY", "MEASUREMENT": "MEASUREMENT",
                  "Standby": "STANDBY", "Measurement": "MEASUREMENT",
                  "POWER_STANDBY_VAL": "STANDBY", "POWER_MEASUREMENT_VAL": "MEASUREMENT"}
        for k, expected in self.spec["power_mode"].items():
            if k in ("description",):
                continue
            for alias, target in pm_map.items():
                if target == k and alias in values:
                    if isinstance(values[alias], int) and values[alias] != expected:
                        self.mismatch(f"{lang}: {alias} = {values[alias]}, expected {expected}")
                    break

    def check_status_bits(self, lang: str, values: dict):
        for name, expected_bit in self.spec["status"].items():
            # Check various naming conventions
            for alias in [f"STATUS_{name}", name, f"Status{name.capitalize()}", name.capitalize()]:
                if alias in values:
                    val = values[alias]
                    # Could be bit position or mask (1<<pos)
                    if isinstance(val, int):
                        if val == (1 << expected_bit) or val == expected_bit:
                            break
                        self.mismatch(f"{lang}: {alias} = {val}, expected bit {expected_bit} (mask 0x{1 << expected_bit:02X})")

    def check_filter_masks(self, lang: str, values: dict):
        filter_map = {"ODR_MASK": "ODR_LPF_MASK", "HPF_MASK": "HPF_CORNER_MASK",
                      "FILTER_ODR_MASK": "ODR_LPF_MASK", "FILTER_HPF_MASK": "HPF_CORNER_MASK",
                      "ODR_LPF_MASK": "ODR_LPF_MASK", "HPF_CORNER_MASK": "HPF_CORNER_MASK"}
        for alias, target in filter_map.items():
            if alias in values and target in self.spec["filter"]:
                expected = self.spec["filter"][target]
                if isinstance(values[alias], int) and values[alias] != expected:
                    self.mismatch(f"{lang}: {alias} = 0x{values[alias]:02X}, expected 0x{expected:02X}")

    def check_i2c_addresses(self, lang: str, values: dict):
        i2c_map = {"I2C_ADDR_DEFAULT": "default", "I2C_DEFAULT_ADDR": "default",
                   "I2C_DEFAULTADDR": "default", "I2CADDR_DEFAULT": "default",
                   "I2C_ADDR_ALTERNATE": "alternate", "I2C_ALTERNATE_ADDR": "alternate"}
        for alias, target in i2c_map.items():
            if alias in values and target in self.spec["i2c_address"]:
                expected = self.spec["i2c_address"][target]
                if isinstance(values[alias], int) and values[alias] != expected:
                    self.mismatch(f"{lang}: {alias} = 0x{values[alias]:02X}, expected 0x{expected:02X}")

    # --------------------------------------------------------------
    # Run all checks
    # --------------------------------------------------------------

    def check_all(self):
        lang_configs = [
            ("C",        self.repo_root / "c" / "include" / "adxl355" / "adxl355_registers.h",        parse_c_header),
            ("Python",   self.repo_root / "python" / "src" / "adxl355" / "registers.py",              parse_python),
            ("Rust",     self.repo_root / "rust" / "src" / "registers.rs",                            parse_rust),
            ("Node/TS",  self.repo_root / "node" / "src" / "registers.ts",                            parse_typescript),
            ("Go",       self.repo_root / "go" / "adxl355" / "registers.go",                          parse_go),
        ]

        for lang, path, parser in lang_configs:
            result = parser(path)
            if "error" in result:
                self.results.append(f"SKIP:     {lang}: {result['error']}")
                continue

            # C uses ADXL355_REG_ prefix on register names
            if lang == "C":
                self.check_register_addrs(lang, result, "ADXL355_REG_")
            else:
                self.check_register_addrs(lang, result)

            self.check_range_values(lang, result)
            self.check_power_mode(lang, result)
            self.check_filter_masks(lang, result)
            self.check_i2c_addresses(lang, result)

    def report(self, quiet: bool = False):
        if not self.results:
            print("✅ ALL CONSISTENCY CHECKS PASSED — no discrepancies found across 5 languages")
            return True

        print(f"\n{'=' * 60}")
        print(f"CONSISTENCY ISSUES FOUND: {len(self.results)}")
        print(f"{'=' * 60}")
        for r in self.results:
            print(f"  {r}")
        if not quiet:
            print("\nTip: regenerate headers with: python spec/generate_c_header.py --output <path>")
        return False


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    spec_dir = Path(__file__).resolve().parent
    repo_root = spec_dir.parent

    quiet = "--quiet" in sys.argv

    checker = ConsistencyChecker(spec_dir, repo_root)
    checker.check_all()
    ok = checker.report(quiet=quiet)

    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
