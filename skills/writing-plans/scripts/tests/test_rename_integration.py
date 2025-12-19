#!/usr/bin/env python3
"""
Integration test for rename_jot.py with lock file cleanup.

Tests the full rename_jot.py script to ensure lock file cleanup
works correctly with nested git repositories.
"""
import sys
import tempfile
import subprocess
from pathlib import Path

# Get path to rename_jot.py
RENAME_SCRIPT = Path(__file__).parent.parent / "rename_jot.py"


def test_rename_with_nested_git_cleanup():
    """Integration test: Full rename with nested git repo lock cleanup."""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create main repo structure
        main_repo = tmpdir / "project"
        main_repo.mkdir()
        (main_repo / ".git").mkdir()

        # Create nested git repo (llm/)
        llm_dir = main_repo / "llm" / "implementation-plans"
        llm_dir.mkdir(parents=True)
        (main_repo / "llm" / ".git").mkdir()

        # Create lock file in main repo root
        lock_file = main_repo / ".writing-plans-active"
        lock_file.write_text("test-plan.md\ncreated: 2025-12-18T12:00:00\n")

        # Create a plan file in nested repo
        plan_file = llm_dir / "my-feature.md"
        plan_file.write_text("""<!-- jot:md-rename -->
---
title: My Feature Implementation
date: 2025-12-18
type: implementation-plan
status: draft
tags: [feature, test]
---

# My Feature Implementation

Test implementation plan.
""")

        # Run rename_jot.py
        result = subprocess.run(
            [sys.executable, str(RENAME_SCRIPT), str(plan_file)],
            capture_output=True,
            text=True
        )

        # Verify rename succeeded
        assert result.returncode == 0, f"Rename failed: {result.stderr}"

        # Verify file was renamed (format: YYMMDD-XX-slug.md)
        renamed_files = list(llm_dir.glob("*-my-feature-implementation.md"))
        assert len(renamed_files) == 1, f"Expected 1 renamed file, found {len(renamed_files)}"

        # Verify lock file was removed from MAIN repo root (not nested repo)
        assert not lock_file.exists(), "Lock file should be removed from main repo root"

        # Verify no lock file in nested repo either
        nested_lock = main_repo / "llm" / ".writing-plans-active"
        assert not nested_lock.exists(), "No lock file should exist in nested repo"

        print("✓ Integration test passed: Rename with nested git repo lock cleanup")


def test_rename_with_single_git_cleanup():
    """Integration test: Full rename with single git repo lock cleanup."""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create single repo structure (no nested git)
        main_repo = tmpdir / "project"
        main_repo.mkdir()
        (main_repo / ".git").mkdir()

        llm_dir = main_repo / "llm" / "implementation-plans"
        llm_dir.mkdir(parents=True)
        # No .git in llm/

        # Create lock file in main repo root
        lock_file = main_repo / ".writing-plans-active"
        lock_file.write_text("test-plan.md\ncreated: 2025-12-18T12:00:00\n")

        # Create a plan file
        plan_file = llm_dir / "auth-system.md"
        plan_file.write_text("""<!-- jot:md-rename -->
---
title: Authentication System
date: 2025-12-18
type: implementation-plan
status: draft
---

# Authentication System

Auth implementation plan.
""")

        # Run rename_jot.py
        result = subprocess.run(
            [sys.executable, str(RENAME_SCRIPT), str(plan_file)],
            capture_output=True,
            text=True
        )

        # Verify rename succeeded
        assert result.returncode == 0, f"Rename failed: {result.stderr}"

        # Verify file was renamed
        renamed_files = list(llm_dir.glob("*-authentication-system.md"))
        assert len(renamed_files) == 1, f"Expected 1 renamed file, found {len(renamed_files)}"

        # Verify lock file was removed
        assert not lock_file.exists(), "Lock file should be removed from main repo root"

        print("✓ Integration test passed: Rename with single git repo lock cleanup")


if __name__ == "__main__":
    try:
        test_rename_with_nested_git_cleanup()
        test_rename_with_single_git_cleanup()
        print("\n✓ All integration tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Integration test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
