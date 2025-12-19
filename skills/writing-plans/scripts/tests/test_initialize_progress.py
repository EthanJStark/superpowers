#!/usr/bin/env python3
"""Tests for initialize_progress.py"""

from pathlib import Path
import sys
import tempfile

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from initialize_progress import derive_progress_path, initialize_progress


def test_derive_progress_path():
    """Verify progress.md is prefixed with plan slug."""
    plan_file = Path("llm/implementation-plans/251217-01-auth.md")
    progress_file = derive_progress_path(plan_file)

    expected = Path("llm/implementation-plans/251217-01-auth-progress.md")
    assert progress_file == expected, f"Expected {expected}, got {progress_file}"


def test_initialize_from_template():
    """Verify progress file is created from template."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir)

        plan_file = tmp_path / "251217-01-test.md"
        plan_file.write_text("# Test Plan")

        template = tmp_path / "template.md"
        template.write_text("# Progress\n[See llm/target.txt]\nBranch:\nLast Commit:\nYYYY-MM-DD")

        progress_file = initialize_progress(
            plan_file=plan_file,
            template_path=template,
            branch="feature/test",
            commit_sha="abc123"
        )

        content = progress_file.read_text()
        assert str(plan_file) in content, f"Expected plan path in content"
        assert "Branch: feature/test" in content, f"Expected branch in content"
        assert "Last Commit: abc123" in content, f"Expected commit in content"
        assert "YYYY-MM-DD" not in content, f"Expected date to be filled in"


if __name__ == "__main__":
    # Simple test runner
    failed = []

    try:
        test_derive_progress_path()
        print("✓ test_derive_progress_path PASSED")
    except Exception as e:
        print(f"✗ test_derive_progress_path FAILED: {e}")
        failed.append("test_derive_progress_path")

    try:
        test_initialize_from_template()
        print("✓ test_initialize_from_template PASSED")
    except Exception as e:
        print(f"✗ test_initialize_from_template FAILED: {e}")
        failed.append("test_initialize_from_template")

    if failed:
        print(f"\n{len(failed)} test(s) failed")
        sys.exit(1)
    else:
        print("\nAll tests passed!")
