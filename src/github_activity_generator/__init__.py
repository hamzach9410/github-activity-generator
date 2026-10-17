"""GitHub Activity & Contribution Generator."""

from .constants import APP_NAME, VERSION
from .core import build_schedule, execute_schedule, is_git_repository

__version__ = VERSION
__all__ = ["build_schedule", "execute_schedule", "is_git_repository", "VERSION", "APP_NAME"]
