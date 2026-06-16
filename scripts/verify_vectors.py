#!/usr/bin/env python3
"""
Cross-language test vector verification.

Loads spec/test_vectors.json and verifies the Python implementation
produces correct results. Optionally triggers other language test
suites to confirm consistency.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
VECTORS_PATH = REPO_ROOT / "spec" / "test_vectors.json"


def load_vectors():
    with open(VECTORS_PATH) as f:
        return json.load(f)


def verify_python(vectors):
    """Verify Python adxl355 package against shared test vectors."""
    sys.path.insert(0, str(REPO_ROOT / "python" / "src"))
    try:
        from adxl355._decode import decode_raw20, raw_to_g, raw_to_mps2
    except ImportError:
        print("  SKIP: Python package not installed (pip install -e python/)")
        return [], 0, 0

    results = []
    tol_g = vectors["acceleration_conversion"]["tolerance_g"]
    tol_m2 = vectors["acceleration_conversion"]["tolerance_mps2"]
    rng_map = {"G2": 0, "G4": 1, "G8": 2}

    for v in vectors["raw_decode"]:
        b = v["bytes"]
        got = decode_raw20(b[0], b[1], b[2])
        ok = got == v["raw"]
        results.append(("Python", f"decode20/{v['name']}", ok, got, v["raw"]))
        if not ok:
            print(f"  FAIL decode20/{v['name']}: got {got}, want {v['raw']}")

    for v in vectors["acceleration_conversion"]["vectors"]:
        rng = rng_map[v["range"]]
        got_g = raw_to_g(v["raw"], rng)
        got_m = raw_to_mps2(v["raw"], rng)
        ok_g = abs(got_g - v["expected_g"]) < tol_g
        ok_m = abs(got_m - v["expected_mps2"]) < tol_m2
        results.append(("Python", f"g/{v['name']}", ok_g, got_g, v["expected_g"]))
        results.append(("Python", f"mps2/{v['name']}", ok_m, got_m, v["expected_mps2"]))
        if not ok_g:
            print(f"  FAIL g/{v['name']}: got {got_g}, want {v['expected_g']}")
        if not ok_m:
            print(f"  FAIL mps2/{v['name']}: got {got_m}, want {v['expected_mps2']}")

    passed = sum(1 for r in results if r[2])
    failed = sum(1 for r in results if not r[2])
    return results, passed, failed


def run_test(cmd, cwd, label):
    """Run a test command and report pass/fail."""
    try:
        result = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=120
        )
        if result.returncode == 0:
            print(f"  {label}: PASS")
            return label, 1, 0
        else:
            print(f"  {label}: FAIL (exit {result.returncode})")
            for line in result.stderr.splitlines()[-5:]:
                print(f"    {line}")
            return label, 0, 1
    except FileNotFoundError as e:
        print(f"  {label}: SKIP ({e})")
        return label, 0, 0
    except subprocess.TimeoutExpired:
        print(f"  {label}: TIMEOUT")
        return label, 0, 1


def main():
    vectors = load_vectors()
    n_decode = len(vectors["raw_decode"])
    n_conv = len(vectors["acceleration_conversion"]["vectors"])
    print(f"Spec: {VECTORS_PATH}")
    print(f"Vectors: {n_decode} decode + {n_conv} conversion")
    print()

    all_results = []

    print("── Python vector verification ──")
    py_results, py_pass, py_fail = verify_python(vectors)
    all_results.extend(py_results)
    print(f"  Python vectors: {py_pass}/{py_pass + py_fail} passed")

    print("\n── Language test suites ──")

    # Python
    print("\n  Python (pytest)...")
    all_results.append(run_test(
        ["python", "-m", "pytest", "-q", "--tb=short"],
        REPO_ROOT / "python", "pytest"
    ))

    # Rust
    print("  Rust (cargo test)...")
    all_results.append(run_test(
        ["cargo", "test", "-q"], REPO_ROOT / "rust", "cargo test"
    ))

    # Go
    print("  Go (go test)...")
    all_results.append(run_test(
        ["go", "test", "./..."], REPO_ROOT / "go", "go test"
    ))

    # Node
    print("  Node (vitest)...")
    all_results.append(run_test(
        ["npx", "vitest", "run"], REPO_ROOT / "node", "vitest"
    ))

    # C
    print("  C (ctest)...")
    all_results.append(run_test(
        ["ctest", "--test-dir", "build", "--output-on-failure"],
        REPO_ROOT / "c", "ctest (C)"
    ))

    # C++ (needs C core build)
    c_core_built = (REPO_ROOT / "c" / "build").exists()
    if c_core_built:
        print("  C++ (ctest)...")
        all_results.append(run_test(
            ["ctest", "--test-dir", "build", "-C", "Debug", "--output-on-failure"],
            REPO_ROOT / "cpp", "ctest (C++)"
        ))
    else:
        print("  C++: SKIP (build C core first)")

    # Summary
    print(f"\n{'=' * 50}")
    total_pass = sum(r[1] for r in all_results if isinstance(r[1], int))
    total_fail = sum(r[2] for r in all_results if isinstance(r[2], int))
    total = total_pass + total_fail
    print(f"Total: {total_pass}/{total} passed")
    if total_fail:
        print(f"FAILURES: {total_fail}")
        return 1
    print("All checks passed!")
    return 0


if __name__ == "__main__":
    sys.exit(main())

