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


if __name__ == "__main__":
    try:
        test_path_resolution_with_different_cwd()
        print("\n✓ All tests passed")
        sys.exit(0)
    except Exception as e:
        print(f"\n✗ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
