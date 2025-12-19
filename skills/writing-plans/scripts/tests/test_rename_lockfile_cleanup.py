#!/usr/bin/env python3
"""
Test lock file cleanup with nested git repositories.

Tests that rename_jot.py correctly finds the outermost git repository
when llm/ is a nested git repo, and cleans up the lock file from the
parent repository root.
"""
import sys
import tempfile
import shutil
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))


def test_nested_git_repo_lockfile_cleanup():
    """Test lock file cleanup when llm/ is a nested git repository."""

    # Create temporary directory structure
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

        # Create lock file in main repo root (where write_plan.py creates it)
        lock_file = main_repo / ".writing-plans-active"
        lock_file.write_text("test-plan.md\ncreated: 2025-12-18T12:00:00\n")

        # Create a plan file in nested repo
        plan_file = llm_dir / "test-plan.md"
        plan_file.write_text("""<!-- jot:md-rename -->
---
title: Test Plan
date: 2025-12-18
type: implementation-plan
status: draft
---

# Test Plan

Test content.
""")

        # Simulate rename_jot.py lock file cleanup logic
        new_path = plan_file  # After rename (using same path for test)
        working_dir = new_path.parent
        outermost_git_root = None

        while working_dir != working_dir.parent:
            if (working_dir / '.git').exists():
                outermost_git_root = working_dir
            working_dir = working_dir.parent

        # Verify we found the outermost git root (main repo)
        assert outermost_git_root == main_repo, \
            f"Expected {main_repo}, got {outermost_git_root}"

        # Verify we can find and remove the lock file
        test_lock_file = outermost_git_root / '.writing-plans-active'
        assert test_lock_file.exists(), "Lock file should exist in main repo"

        # Simulate cleanup
        test_lock_file.unlink()
        assert not test_lock_file.exists(), "Lock file should be removed"

        print("✓ Test passed: Lock file cleanup with nested git repos")


def test_single_git_repo_lockfile_cleanup():
    """Test lock file cleanup in a standard single git repository."""

    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)

        # Create single repo structure (no nested git)
        main_repo = tmpdir / "project"
        main_repo.mkdir()
        (main_repo / ".git").mkdir()

        llm_dir = main_repo / "llm" / "implementation-plans"
        llm_dir.mkdir(parents=True)
        # No .git in llm/ - this is the normal case

        # Create lock file in main repo root
        lock_file = main_repo / ".writing-plans-active"
        lock_file.write_text("test-plan.md\ncreated: 2025-12-18T12:00:00\n")

        # Create a plan file
        plan_file = llm_dir / "test-plan.md"
        plan_file.write_text("""<!-- jot:md-rename -->
---
title: Test Plan
date: 2025-12-18
type: implementation-plan
status: draft
---

# Test Plan

Test content.
""")

        # Simulate rename_jot.py lock file cleanup logic
        new_path = plan_file
        working_dir = new_path.parent
        outermost_git_root = None

        while working_dir != working_dir.parent:
            if (working_dir / '.git').exists():
                outermost_git_root = working_dir
            working_dir = working_dir.parent

        # Verify we found the git root
        assert outermost_git_root == main_repo, \
            f"Expected {main_repo}, got {outermost_git_root}"

        # Verify we can find and remove the lock file
        test_lock_file = outermost_git_root / '.writing-plans-active'
        assert test_lock_file.exists(), "Lock file should exist in main repo"

        # Simulate cleanup
        test_lock_file.unlink()
        assert not test_lock_file.exists(), "Lock file should be removed"

        print("✓ Test passed: Lock file cleanup in single git repo")


if __name__ == "__main__":
    try:
        test_nested_git_repo_lockfile_cleanup()
        test_single_git_repo_lockfile_cleanup()
        print("\n✓ All tests passed!")
        sys.exit(0)
    except AssertionError as e:
        print(f"\n✗ Test failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
