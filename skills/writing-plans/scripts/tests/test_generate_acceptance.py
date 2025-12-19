#!/usr/bin/env python3
"""Tests for generate_acceptance.py"""

from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from generate_acceptance import derive_acceptance_path


def test_output_path_derived_from_plan_name():
    """Verify acceptance.json is prefixed with plan slug."""
    plan_file = Path("llm/implementation-plans/251217-01-auth.md")
    output_file = derive_acceptance_path(plan_file)

    expected = Path("llm/implementation-plans/251217-01-auth-acceptance.json")
    assert output_file == expected, f"Expected {expected}, got {output_file}"


if __name__ == "__main__":
    # Simple test runner
    try:
        test_output_path_derived_from_plan_name()
        print("✓ test_output_path_derived_from_plan_name PASSED")
    except Exception as e:
        print(f"✗ test_output_path_derived_from_plan_name FAILED: {e}")
        sys.exit(1)
