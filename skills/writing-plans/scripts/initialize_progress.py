#!/usr/bin/env python3
"""
Initialize per-plan progress.md from template.

Replaces generic llm/progress.md with plan-prefixed version.
"""
import argparse
import subprocess
from datetime import date
from pathlib import Path


def derive_progress_path(plan_file: Path) -> Path:
    """
    Derive progress.md path from plan filename.

    Input:  llm/implementation-plans/251217-01-auth.md
    Output: llm/implementation-plans/251217-01-auth-progress.md
    """
    stem = plan_file.stem
    parent = plan_file.parent
    return parent / f"{stem}-progress.md"


def get_git_info():
    """Get current branch and commit SHA."""
    try:
        branch = subprocess.check_output(
            ['git', 'branch', '--show-current'],
            text=True
        ).strip()

        commit = subprocess.check_output(
            ['git', 'rev-parse', '--short', 'HEAD'],
            text=True
        ).strip()

        return branch, commit
    except subprocess.CalledProcessError:
        return "unknown", "unknown"


def initialize_progress(
    plan_file: Path,
    template_path: Path,
    branch: str = None,
    commit_sha: str = None
) -> Path:
    """
    Create progress.md from template with filled placeholders.

    Returns path to created progress file.
    """
    progress_file = derive_progress_path(plan_file)

    # Get git info if not provided
    if branch is None or commit_sha is None:
        branch, commit_sha = get_git_info()

    # Read template
    template = template_path.read_text()

    # Fill placeholders
    content = template.replace(
        '[See llm/target.txt]',
        str(plan_file)
    ).replace(
        'Branch:',
        f'Branch: {branch}'
    ).replace(
        'Last Commit:',
        f'Last Commit: {commit_sha}'
    ).replace(
        'YYYY-MM-DD',
        date.today().isoformat()
    )

    # Write progress file
    progress_file.write_text(content)

    return progress_file


def main():
    parser = argparse.ArgumentParser(
        description='Initialize per-plan progress.md'
    )
    parser.add_argument(
        '--plan-file',
        required=True,
        type=Path,
        help='Plan file (e.g., 251217-01-auth.md)'
    )
    parser.add_argument(
        '--template',
        type=Path,
        default=Path.home() / '.claude/templates/progress.md',
        help='Template path (default: ~/.claude/templates/progress.md)'
    )
    args = parser.parse_args()

    if not args.plan_file.exists():
        print(f"ERROR: Plan file not found: {args.plan_file}")
        return 1

    if not args.template.exists():
        print(f"ERROR: Template not found: {args.template}")
        print("  Expected at: ~/.claude/templates/progress.md")
        return 1

    progress_file = initialize_progress(args.plan_file, args.template)
    print(f"✓ Initialized progress log: {progress_file}")

    return 0


if __name__ == '__main__':
    exit(main())
