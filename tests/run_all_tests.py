"""
Comprehensive Test Runner for MDAN

This script runs all integration tests to verify all agents are working correctly.
"""

import sys
import os
import subprocess


def run_test(test_file, description):
    """Run a test file and return the result."""
    print(f"\n{'=' * 60}")
    print(f"Running: {description}")
    print(f"{'=' * 60}\n")

    result = subprocess.run([sys.executable, test_file], capture_output=True, text=True)

    if result.returncode == 0:
        print(f"✓ {description} - PASSED")
        return True
    else:
        print(f"✗ {description} - FAILED")
        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)
        return False


def main():
    """Run all integration tests."""
    print("\n" + "=" * 60)
    print("MDAN - Comprehensive Integration Test Suite")
    print("=" * 60 + "\n")

    tests = [
        ("tests/simple_test.py", "Core (MDAN Master)"),
        ("tests/simple_fintech_test.py", "FinTech Pack"),
        ("tests/simple_devops_test.py", "DevOps/Azure Pack"),
        ("tests/simple_mmb_test.py", "MMB Module"),
        ("tests/simple_cis_test.py", "CIS Module"),
        ("tests/simple_tea_test.py", "TEA Module"),
        ("tests/simple_ux_designer_test.py", "UX Designer (MMM)"),
    ]

    results = []
    for test_file, description in tests:
        if os.path.exists(test_file):
            result = run_test(test_file, description)
            results.append((description, result))
        else:
            print(f"⚠ {description} - Test file not found: {test_file}")
            results.append((description, False))

    # Print summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60 + "\n")

    passed = sum(1 for _, result in results if result)
    total = len(results)

    for description, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {description}")

    print("\n" + "=" * 60)
    print(f"Results: {passed}/{total} tests passed")
    print("=" * 60 + "\n")

    if passed == total:
        print("🎉 All integration tests passed!")
        return 0
    else:
        print(f"⚠ {total - passed} test(s) failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
