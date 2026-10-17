#!/usr/bin/env python3
"""
GitHub Activity & Contribution Generator
A customizable tool to generate Git commit histories and simulate contribution activity.
"""

import argparse
import os
import random
import subprocess
import sys
from datetime import datetime, date, timedelta

DEFAULT_COMMIT_MESSAGES = [
    "Refactor data parsing utilities",
    "Update documentation and code structure",
    "Fix edge cases in validation logic",
    "Enhance performance metrics and execution time",
    "Routine maintenance and updates",
    "Improve error handling and fallback routines",
    "Clean up codebase and remove unused functions",
    "Update unit tests and assertion checks",
    "Optimize data processing pipeline",
    "Refactor helper modules for better readability",
    "Update configuration defaults and logging",
    "Resolve minor warnings and code linting",
    "Improve response caching mechanism",
    "Streamline internal utility methods",
    "Add boundary checks to input processing",
    "Update build configuration and dependencies",
    "Refactor state management in worker routines",
    "Improve logging consistency across modules",
    "Optimize memory footprint during data processing",
    "Update API client timeouts and retries",
]


def is_git_repository(path="."):
    """Verifies that the target path is inside a git repository."""
    try:
        subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def generate_activity(
    start_date: date,
    end_date: date,
    min_commits: int = 2,
    max_commits: int = 5,
    weekdays_only: bool = True,
    chance_active: float = 0.88,
    work_hours: tuple = (9, 21),
    filename: str = "activity_log.txt",
    repo_path: str = ".",
    dry_run: bool = False,
):
    """Generates commits across the date range."""
    if not dry_run and not is_git_repository(repo_path):
        print("❌ Error: Target directory is not a git repository. Initialize git first (`git init`).")
        sys.exit(1)

    cur_date = start_date
    planned_commits = []

    start_sec = work_hours[0] * 3600
    end_sec = work_hours[1] * 3600

    while cur_date <= end_date:
        if weekdays_only and cur_date.weekday() >= 5:
            cur_date += timedelta(days=1)
            continue

        if random.random() <= chance_active:
            daily_count = random.randint(min_commits, max_commits)
            day_seconds = sorted(random.sample(range(start_sec, end_sec), daily_count))

            for sec in day_seconds:
                dt = datetime(cur_date.year, cur_date.month, cur_date.day) + timedelta(seconds=sec)
                msg = random.choice(DEFAULT_COMMIT_MESSAGES)
                planned_commits.append((dt, msg))

        cur_date += timedelta(days=1)

    # Strictly monotonic order
    for i in range(1, len(planned_commits)):
        if planned_commits[i][0] <= planned_commits[i - 1][0]:
            planned_commits[i] = (
                planned_commits[i - 1][0] + timedelta(minutes=random.randint(15, 60)),
                planned_commits[i][1],
            )

    total_days = (end_date - start_date).days + 1
    active_days = len(set(c[0].date() for c in planned_commits))

    print(f"\n📊 Generation Plan:")
    print(f"  • Date range: {start_date} to {end_date} ({total_days} days)")
    print(f"  • Active commit days: {active_days}")
    print(f"  • Total commits: {len(planned_commits)}")
    print(f"  • Weekdays only: {weekdays_only}")
    print(f"  • Daily commit range: {min_commits} - {max_commits}")

    if dry_run:
        print("\n🔍 Dry-run mode enabled. No commits were created.")
        if planned_commits:
            print("\nSample Preview (First 5 commits):")
            for dt, msg in planned_commits[:5]:
                print(f"  [{dt.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
            print("...")
            print("Sample Preview (Last 3 commits):")
            for dt, msg in planned_commits[-3:]:
                print(f"  [{dt.strftime('%Y-%m-%d %H:%M:%S')}] {msg}")
        return

    filepath = os.path.join(repo_path, filename)
    env = os.environ.copy()

    print(f"\n🚀 Creating {len(planned_commits)} commits in '{repo_path}'...")
    for idx, (dt, msg) in enumerate(planned_commits, start=1):
        iso_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

        with open(filepath, "a") as f:
            f.write(f"[{iso_str}] {msg}\n")

        subprocess.run(
            ["git", "add", filename],
            cwd=repo_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        env["GIT_AUTHOR_DATE"] = iso_str
        env["GIT_COMMITTER_DATE"] = iso_str

        subprocess.run(
            ["git", "commit", "-m", msg],
            cwd=repo_path,
            env=env,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        if idx % 100 == 0 or idx == len(planned_commits):
            progress = (idx / len(planned_commits)) * 100
            print(f"  Progress: {idx}/{len(planned_commits)} ({progress:.1f}%)")

    print("\n✅ Successfully created all commits!")
    print("Run `git push origin main` (or your target branch) to update remote.")


def parse_date(date_str: str) -> date:
    """Parses YYYY-MM-DD date string."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format '{date_str}'. Use YYYY-MM-DD.")


def main():
    parser = argparse.ArgumentParser(
        description="GitHub Activity & Contribution Generator: Create customizable, professional Git commit histories.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    default_start = (date.today() - timedelta(days=180)).strftime("%Y-%m-%d")
    default_end = date.today().strftime("%Y-%m-%d")

    parser.add_argument(
        "--start-date",
        type=parse_date,
        default=default_start,
        help=f"Start date in YYYY-MM-DD format (default: {default_start})",
    )
    parser.add_argument(
        "--end-date",
        type=parse_date,
        default=default_end,
        help=f"End date in YYYY-MM-DD format (default: today, {default_end})",
    )
    parser.add_argument(
        "--min-commits",
        type=int,
        default=2,
        help="Minimum commits per active day (default: 2)",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=5,
        help="Maximum commits per active day (default: 5)",
    )
    parser.add_argument(
        "--include-weekends",
        action="store_true",
        help="Include Saturdays and Sundays (default: weekdays only)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview plan and commit schedule without touching git",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Path to git repository (default: current directory)",
    )

    args = parser.parse_args()

    if args.start_date > args.end_date:
        print("❌ Error: --start-date must be before or equal to --end-date.")
        sys.exit(1)

    if args.end_date > date.today():
        print(f"⚠️ Warning: --end-date ({args.end_date}) is in the future. Commits after today ({date.today()}) look unnatural on GitHub profiles.")

    generate_activity(
        start_date=args.start_date,
        end_date=args.end_date,
        min_commits=args.min_commits,
        max_commits=args.max_commits,
        weekdays_only=not args.include_weekends,
        repo_path=args.path,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    main()
