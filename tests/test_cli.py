"""Unit tests for CLI parsing and validation."""

import unittest
from datetime import date
import argparse
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from github_activity_generator.cli import parse_date


class TestCLIParsing(unittest.TestCase):
    def test_parse_valid_date(self):
        result = parse_date("2026-10-18")
        self.assertEqual(result, date(2026, 10, 18))

    def test_parse_invalid_date_format(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_date("18-10-2026")

    def test_parse_non_date_string(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            parse_date("not-a-date")


if __name__ == "__main__":
    unittest.main()
