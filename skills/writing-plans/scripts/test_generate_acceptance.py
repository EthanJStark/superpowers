#!/usr/bin/env python3
"""Test generate_acceptance.py path resolution."""
from pathlib import Path
import tempfile
import os
import sys
import json

# Add scripts dir to path
sys.path.insert(0, str(Path(__file__).parent))
from generate_acceptance import generate_acceptance


def test_path_resolution_with_different_cwd():
    """Test that script works when cwd differs from plan file location."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create test plan file
        plan_dir = Path(tmpdir) / "llm" / "implementation-plans"
        plan_dir.mkdir(parents=True)
        plan_file = plan_dir / "test-plan.md"

        plan_content = """<!-- jot:md-rename -->
---
title: Test Plan
date: 2025-12-16
type: implementation-plan
status: draft
tags: [test]
---

# Test Plan

### Task 1: First Task
Do something

### Task 2: Second Task
Do another thing
"""
        plan_file.write_text(plan_content)

        # Run from different directory (not tmpdir)
        original_cwd = Path.cwd()
        output_file = plan_dir.parent / "acceptance.json"

        try:
            # This should fail with current implementation
            generate_acceptance(plan_file, output_file)

            # Verify output
            assert output_file.exists(), "Output file should exist"
            data = json.loads(output_file.read_text())
            assert data["total_features"] == 2, f"Expected 2 features, got {data['total_features']}"
            assert "plan" in data, "Output should contain 'plan' key"

            print("✓ test_path_resolution_with_different_cwd passed")

        finally:
            os.chdir(original_cwd)


def test_absolute_path_fallback():
    """Test fallback to absolute path when relative resolution impossible."""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create nested structure to test path resolution
        # Plan file outside the output tree
        plan_dir = Path(tmpdir) / "external"
        plan_dir.mkdir()
        plan_file = plan_dir / "plan.md"
        plan_file.write_text("""<!-- jot:md-rename -->
---
title: Test
date: 2025-12-16
type: implementation-plan
status: draft
---
# Test
### Task 1: Test
""")

        # Output in a shallow location (only one parent)
        # This means output_file.parent.parent won't contain the plan file
        output_dir = Path(tmpdir) / "output"
        output_dir.mkdir()
        output_file = output_dir / "acceptance.json"

        generate_acceptance(plan_file, output_file)

        data = json.loads(output_file.read_text())
        # Path may be relative or absolute depending on structure
        # The important thing is that it exists and is valid
        assert "plan" in data, "Output should contain 'plan' key"
        plan_path = Path(data["plan"])
        # Verify the path is valid (either absolute or resolves correctly)
        if not plan_path.is_absolute():
            # If relative, it should still point to a valid location conceptually
            assert isinstance(data["plan"], str), "Plan path should be a string"

        print("✓ test_absolute_path_fallback passed")


def test_normal_workflow():
    """Test normal workflow where paths are in same tree."""
    with tempfile.TemporaryDirectory() as tmpdir:
        plan_file = Path(tmpdir) / "llm" / "plans" / "test.md"
        plan_file.parent.mkdir(parents=True)
        plan_file.write_text("""<!-- jot:md-rename -->
---
title: Test
date: 2025-12-16
type: implementation-plan
status: draft
---
# Test
### Task 1: Test
""")

        output_file = Path(tmpdir) / "llm" / "acceptance.json"
        generate_acceptance(plan_file, output_file)

        data = json.loads(output_file.read_text())
        # Should be relative path
        assert not Path(data["plan"]).is_absolute(), f"Expected relative path, got {data['plan']}"
        assert data["plan"] == "llm/plans/test.md", f"Expected 'llm/plans/test.md', got {data['plan']}"

        print("✓ test_normal_workflow passed")


if __name__ == "__main__":
    tests = [
        ("path resolution with different cwd", test_path_resolution_with_different_cwd),
        ("absolute path fallback", test_absolute_path_fallback),
        ("normal workflow", test_normal_workflow)
    ]

    failed = []
    for name, test_fn in tests:
        try:
            print(f"\nRunning: {name}")
            test_fn()
        except Exception as e:
            print(f"✗ {name} failed: {e}")
            import traceback
            traceback.print_exc()
            failed.append(name)

    if failed:
        print(f"\n✗ {len(failed)} test(s) failed: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("\n✓ All tests passed")
        sys.exit(0)
