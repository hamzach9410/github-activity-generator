"""Command-line interface for GitHub Activity Generator."""

import argparse
import sys
from datetime import datetime, date, timedelta

from .constants import APP_NAME, VERSION
from .core import build_schedule, execute_schedule, is_git_repository


def parse_date(date_str: str) -> date:
    """Parses YYYY-MM-DD date string."""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format '{date_str}'. Expected YYYY-MM-DD.")


def print_banner():
    """Prints tool header."""
    print("=" * 65)
    print(f"  {APP_NAME} v{VERSION}")
    print("  Natural Multi-File Commits & Contribution Generator")
    print("=" * 65)


def main():
    parser = argparse.ArgumentParser(
        description=f"{APP_NAME}: Create customizable, multi-file Git commit histories with natural scheduling.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    default_start = (date.today() - timedelta(days=90)).strftime("%Y-%m-%d")
    default_end = date.today().strftime("%Y-%m-%d")

    parser.add_argument(
        "--start-date",
        type=parse_date,
        default=default_start,
        help=f"Start date in YYYY-MM-DD format (default: 90 days ago, {default_start})",
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
        help="Minimum commits on active days (default: 2)",
    )
    parser.add_argument(
        "--max-commits",
        type=int,
        default=5,
        help="Maximum commits on active days (default: 5)",
    )
    parser.add_argument(
        "--include-weekends",
        action="store_true",
        help="Include Saturdays and Sundays (default: weekdays only)",
    )
    parser.add_argument(
        "--single-file",
        type=str,
        default=None,
        help="Restrict all commits to a single file path instead of rotating across project files",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview schedule and target files without creating Git commits",
    )
    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Target Git repository directory (default: current directory)",
    )

    args = parser.parse_args()

    print_banner()

    if args.start_date > args.end_date:
        print("❌ Error: --start-date must be earlier than or equal to --end-date.")
        sys.exit(1)

    if args.end_date > date.today():
        print(f"⚠️ Warning: --end-date ({args.end_date}) is in the future. Commits after today ({date.today()}) look unnatural on GitHub profiles.")

    if not args.dry_run and not is_git_repository(args.path):
        print(f"❌ Error: '{args.path}' is not a valid Git repository.")
        print("Initialize git first with `git init` or specify a valid repository path with `--path`.")
        sys.exit(1)

    weekdays_only = not args.include_weekends

    planned = build_schedule(
        start_date=args.start_date,
        end_date=args.end_date,
        min_commits=args.min_commits,
        max_commits=args.max_commits,
        weekdays_only=weekdays_only,
        single_file=args.single_file,
    )

    total_days = (args.end_date - args.start_date).days + 1
    active_days = len(set(c.dt.date() for c in planned))
    unique_files = len(set(c.target_file for c in planned))

    print("\n📋 Plan Details:")
    print(f"  • Date Range:        {args.start_date} to {args.end_date} ({total_days} days)")
    print(f"  • Active Days:       {active_days}")
    print(f"  • Planned Commits:   {len(planned)}")
    print(f"  • Target Files:      {unique_files} distinct files (multi-file distribution)")
    print(f"  • Weekdays Only:     {weekdays_only}")
    print(f"  • Daily Range:       {args.min_commits} - {args.max_commits} commits/day")

    if args.dry_run:
        print("\n🔍 [DRY-RUN] Previewing planned commits across different files (no changes made):")
        if planned:
            for item in planned[:6]:
                print(f"  ✔ [{item.dt.strftime('%Y-%m-%d %H:%M:%S')}] {item.target_file:<24} -> {item.message}")
            if len(planned) > 9:
                print("  ...")
                for item in planned[-3:]:
                    print(f"  ✔ [{item.dt.strftime('%Y-%m-%d %H:%M:%S')}] {item.target_file:<24} -> {item.message}")
        print("\nExecution complete. Run without '--dry-run' to write commits.")
        return

    print(f"\n🚀 Creating {len(planned)} commits across {unique_files} files in '{args.path}'...")
    try:
        total = execute_schedule(planned, repo_path=args.path)
        print(f"\n✅ Successfully created {total} commits across {unique_files} different project files!")
        print("Next step: Run `git push origin main` (or your target branch) to push to GitHub.")
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
