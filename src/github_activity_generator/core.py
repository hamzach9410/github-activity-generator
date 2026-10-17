"""Core activity generation and Git automation logic."""

import json
import os
import random
import subprocess
import sys
from datetime import datetime, date, timedelta
from typing import List, Tuple, Optional, NamedTuple

from .constants import (
    COMMIT_TEMPLATES,
    DEFAULT_WORK_HOURS,
    DEFAULT_CHANCE_ACTIVE,
)


class CommitPlanItem(NamedTuple):
    """Represents a planned commit with timestamp, target file, and message."""
    dt: datetime
    target_file: str
    message: str


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


def get_flattened_templates() -> List[Tuple[str, str]]:
    """Returns a flat list of (target_file, message) pairs from all categories."""
    flat = []
    for cat, items in COMMIT_TEMPLATES.items():
        flat.extend(items)
    return flat


def build_schedule(
    start_date: date,
    end_date: date,
    min_commits: int = 2,
    max_commits: int = 5,
    weekdays_only: bool = True,
    chance_active: float = DEFAULT_CHANCE_ACTIVE,
    work_hours: Tuple[int, int] = DEFAULT_WORK_HOURS,
    single_file: Optional[str] = None,
    seed: Optional[int] = None,
) -> List[CommitPlanItem]:
    """Builds a sorted list of planned commits across different files."""
    if seed is not None:
        random.seed(seed)

    all_templates = get_flattened_templates()
    cur_date = start_date
    planned_commits: List[CommitPlanItem] = []

    start_sec = work_hours[0] * 3600
    end_sec = work_hours[1] * 3600

    # Pool tracker to avoid consecutive identical files
    last_file = ""

    while cur_date <= end_date:
        if weekdays_only and cur_date.weekday() >= 5:
            cur_date += timedelta(days=1)
            continue

        if random.random() <= chance_active:
            daily_count = random.randint(min_commits, max_commits)
            day_seconds = sorted(random.sample(range(start_sec, end_sec), daily_count))

            for sec in day_seconds:
                dt = datetime(cur_date.year, cur_date.month, cur_date.day) + timedelta(seconds=sec)

                if single_file:
                    target_file = single_file
                    msg = random.choice(all_templates)[1]
                else:
                    # Pick a template with a different target file than the previous commit
                    available = [t for t in all_templates if t[0] != last_file] or all_templates
                    target_file, msg = random.choice(available)
                    last_file = target_file

                planned_commits.append(CommitPlanItem(dt=dt, target_file=target_file, message=msg))

        cur_date += timedelta(days=1)

    # Strictly monotonic ordering guarantee
    for i in range(1, len(planned_commits)):
        if planned_commits[i].dt <= planned_commits[i - 1].dt:
            new_dt = planned_commits[i - 1].dt + timedelta(minutes=random.randint(15, 60))
            planned_commits[i] = CommitPlanItem(
                dt=new_dt,
                target_file=planned_commits[i].target_file,
                message=planned_commits[i].message,
            )

    return planned_commits


def generate_content_for_file(target_file: str, message: str, dt_str: str) -> str:
    """Generates realistic code, documentation, test, or config content based on file extension."""
    if target_file.endswith(".py"):
        func_slug = message.split(":")[-1].strip().lower().replace(" ", "_").replace("-", "_")
        func_slug = "".join(c for c in func_slug if c.isalnum() or c == "_")[:32]
        return (
            f"\n\n# Added on {dt_str}: {message}\n"
            f"def helper_{func_slug}():\n"
            f"    \"\"\"Routine for {message}.\"\"\"\n"
            f"    return True\n"
        )
    elif target_file.endswith(".md"):
        return f"\n\n## Update {dt_str}\n- **Change**: {message}\n- **Status**: Implemented and verified.\n"
    elif target_file.endswith(".json"):
        return f"\n// Update {dt_str}: {message}\n"
    elif target_file.endswith(".sh"):
        return f"\n# Check added on {dt_str}: {message}\necho \"[health] {message}\"\n"
    else:
        return f"[{dt_str}] {message}\n"


def execute_schedule(
    planned_commits: List[CommitPlanItem],
    repo_path: str = ".",
) -> int:
    """Executes Git commits for the planned schedule, modifying corresponding target files."""
    if not is_git_repository(repo_path):
        raise RuntimeError(f"Target path '{repo_path}' is not a valid Git repository.")

    env = os.environ.copy()
    total = len(planned_commits)

    for idx, item in enumerate(planned_commits, start=1):
        iso_str = item.dt.strftime("%Y-%m-%dT%H:%M:%S")
        full_path = os.path.join(repo_path, item.target_file)

        # Ensure target file's parent directories exist
        os.makedirs(os.path.dirname(full_path), exist_ok=True)

        content = generate_content_for_file(item.target_file, item.message, iso_str)

        # Append realistic snippet to target file
        with open(full_path, "a", encoding="utf-8") as f:
            f.write(content)

        subprocess.run(
            ["git", "add", item.target_file],
            cwd=repo_path,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        env["GIT_AUTHOR_DATE"] = iso_str
        env["GIT_COMMITTER_DATE"] = iso_str

        subprocess.run(
            ["git", "commit", "-m", item.message],
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
