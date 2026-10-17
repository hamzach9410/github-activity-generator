"""Core activity generation and Git automation logic."""

import os
import random
import subprocess
import sys
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional

from .constants import (
    DEFAULT_COMMIT_MESSAGES,
    DEFAULT_WORK_HOURS,
    DEFAULT_CHANCE_ACTIVE,
    DEFAULT_FILENAME,
)


def is_git_repository(path: str = ".") -> bool:
    """Verifies that the target path is inside a working Git repository."""
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


def build_schedule(
    start_date: date,
    end_date: date,
    min_commits: int = 2,
    max_commits: int = 5,
    weekdays_only: bool = True,
    chance_active: float = DEFAULT_CHANCE_ACTIVE,
    work_hours: Tuple[int, int] = DEFAULT_WORK_HOURS,
    messages: Optional[List[str]] = None,
    seed: Optional[int] = None,
) -> List[Tuple[datetime, str]]:
    """Builds a sorted list of timestamps and commit messages."""
    if seed is not None:
        random.seed(seed)

    message_pool = messages or DEFAULT_COMMIT_MESSAGES
    cur_date = start_date
    planned_commits: List[Tuple[datetime, str]] = []

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
                msg = random.choice(message_pool)
                planned_commits.append((dt, msg))

        cur_date += timedelta(days=1)

    # Strictly monotonic ordering guarantee
    for i in range(1, len(planned_commits)):
        if planned_commits[i][0] <= planned_commits[i - 1][0]:
            planned_commits[i] = (
                planned_commits[i - 1][0] + timedelta(minutes=random.randint(15, 60)),
                planned_commits[i][1],
            )

    return planned_commits


def execute_schedule(
    planned_commits: List[Tuple[datetime, str]],
    repo_path: str = ".",
    filename: str = DEFAULT_FILENAME,
) -> int:
    """Executes Git commits for the planned schedule."""
    if not is_git_repository(repo_path):
        raise RuntimeError(f"Target path '{repo_path}' is not a valid Git repository.")

    filepath = os.path.join(repo_path, filename)
    env = os.environ.copy()
    total = len(planned_commits)

    for idx, (dt, msg) in enumerate(planned_commits, start=1):
        iso_str = dt.strftime("%Y-%m-%dT%H:%M:%S")

        with open(filepath, "a", encoding="utf-8") as f:
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

        if idx % 50 == 0 or idx == total:
            progress = (idx / total) * 100
            print(f"  [Progress] {idx}/{total} commits created ({progress:.1f}%)")

    return total
