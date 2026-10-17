"""Unit tests for the core scheduling engine."""

import unittest
from datetime import date
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from github_activity_generator.core import build_schedule, CommitPlanItem


class TestCoreSchedule(unittest.TestCase):
    def test_weekdays_only(self):
        """Ensures that weekends are strictly excluded when weekdays_only is True."""
        start = date(2026, 1, 1)
        end = date(2026, 1, 31)
        schedule = build_schedule(start, end, weekdays_only=True, seed=42)

        for item in schedule:
            self.assertLess(item.dt.weekday(), 5, f"Found weekend commit on {item.dt}")

    def test_include_weekends(self):
        """Ensures weekends can be included if requested."""
        start = date(2026, 1, 1)
        end = date(2026, 3, 31)
        schedule = build_schedule(start, end, weekdays_only=False, seed=42)
        has_weekend = any(item.dt.weekday() >= 5 for item in schedule)
        self.assertTrue(has_weekend)

    def test_strictly_monotonic_timestamps(self):
        """Ensures timestamps are in strict chronological order."""
        start = date(2026, 5, 1)
        end = date(2026, 6, 30)
        schedule = build_schedule(start, end, seed=123)

        for i in range(1, len(schedule)):
            self.assertGreater(
                schedule[i].dt,
                schedule[i - 1].dt,
                f"Non-monotonic timestamps: {schedule[i-1].dt} -> {schedule[i].dt}",
            )

    def test_custom_commit_bounds(self):
        """Verifies custom min and max commit boundaries per active day."""
        start = date(2026, 7, 1)
        end = date(2026, 7, 10)
        schedule = build_schedule(start, end, min_commits=3, max_commits=3, seed=77)

        from collections import defaultdict
        by_day = defaultdict(int)
        for item in schedule:
            by_day[item.dt.date()] += 1

        for day, count in by_day.items():
            self.assertEqual(count, 3, f"Day {day} had {count} commits instead of 3")

    def test_multi_file_distribution(self):
        """Ensures commits are distributed across multiple different files."""
        start = date(2026, 5, 1)
        end = date(2026, 6, 30)
        schedule = build_schedule(start, end, seed=99)

        files = set(item.target_file for item in schedule)
        self.assertGreater(len(files), 5, "Expected commits across multiple different files")

        # Verify no consecutive identical files
        consecutive_same = sum(
            1 for i in range(1, len(schedule)) if schedule[i].target_file == schedule[i - 1].target_file
        )
        self.assertEqual(consecutive_same, 0, "Found consecutive commits modifying the same file")

    def test_single_file_override(self):
        """Ensures single_file parameter restricts all commits to one file if requested."""
        start = date(2026, 5, 1)
        end = date(2026, 5, 15)
        schedule = build_schedule(start, end, single_file="notes.txt", seed=42)

        files = set(item.target_file for item in schedule)
        self.assertEqual(files, {"notes.txt"})


if __name__ == "__main__":
    unittest.main()
