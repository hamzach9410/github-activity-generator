#!/usr/bin/env python3
"""Convenience root wrapper for GitHub Activity Generator."""

import sys
import os

# Add src to python path for direct script execution
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from github_activity_generator.cli import main

if __name__ == "__main__":
    main()
