# GitHub Activity & Contribution Generator

A modern, customizable Python CLI tool to simulate Git commit activity and design natural GitHub contribution calendars with realistic, multi-file commits.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/hamzach9410/github-activity-generator/actions/workflows/ci.yml/badge.svg)](https://github.com/hamzach9410/github-activity-generator/actions)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

---

## Visual Preview

![GitHub Activity Generator CLI Demo](assets/demo.png)

---

## Key Features

- **Multi-File Commit Distribution**: Commits are intelligently rotated across realistic project files (`src/*.py`, `docs/*.md`, `tests/test_*.py`, `config/*.json`) rather than touching a single dummy file.
- **Conventional Commits**: Every commit uses standard Conventional Commits syntax (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`, `perf:`, `chore:`) tailored to the specific file changed.
- **Realistic File Content**: Appends actual Python functions, test assertions, markdown documentation, and config settings instead of dummy timestamps.
- **Custom Historical Date Ranges**: Generate commit histories across any range (`--start-date`, `--end-date`).
- **Natural Weekday Scheduling**: Automatically filters out weekends (Saturday & Sunday) to replicate real developer work patterns.
- **Configurable Daily Bounds**: Specify `--min-commits` and `--max-commits` to prevent unnatural volume spikes.
- **Business Hours Distribution**: Commits are generated during realistic daylight and evening hours with randomized spacing.
- **Dry-Run Preview**: Inspect dates, target files, and messages before writing a single Git commit.
- **Zero External Dependencies**: Pure Python standard library. Works out of the box with zero third-party packages.

---

## Project Structure

```text
github-activity-generator/
├── .github/
│   └── workflows/
│       └── ci.yml             # Automated GitHub Actions test workflow
├── assets/
│   └── demo.png               # Terminal execution screenshot
├── src/
│   └── github_activity_generator/
│       ├── __init__.py        # Package exports & version
│       ├── __main__.py        # Entry for python3 -m execution
│       ├── cli.py             # CLI parser and colored output
│       ├── core.py            # Scheduling engine & multi-file Git runner
│       └── constants.py       # File targets & Conventional Commit pools
├── tests/
│   ├── __init__.py
│   ├── test_cli.py            # CLI argument & date parsing unit tests
│   └── test_core.py           # Core scheduling & monotonicity tests
├── .gitignore
├── generator.py               # Root quick-start wrapper
├── LICENSE                    # MIT License
├── pyproject.toml             # Standard PEP 621 packaging
├── README.md                  # Documentation with screenshot & usage guide
└── requirements-dev.txt       # Development dependencies
```

---

## Quickstart

### Option 1: Direct Clone & Run

```bash
git clone https://github.com/hamzach9410/github-activity-generator.git
cd github-activity-generator
```

Run directly with Python:

```bash
# Preview schedule with dry-run
python3 generator.py --dry-run

# Run for past 90 days on weekdays across multiple files
python3 generator.py --start-date 2026-07-01 --end-date 2026-10-18
```

### Option 2: Install as Global CLI via Pip

```bash
pip install -e .
```

Now you can run the command from any repository on your system:

```bash
github-activity-generator --dry-run
github-activity-generator --start-date 2026-01-01 --end-date 2026-06-30 --min-commits 2 --max-commits 4
```

---

## Usage Guide & Examples

### 1. Safe Dry-Run (Always recommended first)
Preview planned dates, target files, and messages without touching your Git repository:

```bash
python3 generator.py --start-date 2026-06-01 --end-date 2026-10-18 --dry-run
```

Sample output:
```text
  ✔ [2026-07-20 09:02:16] CHANGELOG.md             -> docs(changelog): update release notes for v1.1 milestone
  ✔ [2026-07-20 17:44:26] tests/test_formatter.py  -> test(formatter): add regression assertions for duration parser
  ✔ [2026-07-20 18:45:37] src/cache.py             -> feat(cache): add LRU eviction policy with configurable TTL
  ✔ [2026-07-20 19:45:34] config/settings.json     -> chore(config): adjust default connection pool size and timeouts
  ✔ [2026-07-21 14:23:23] src/validators.py        -> fix(validators): sanitize unicode control characters in input
```

### 2. Generate Commits for a Custom Range
```bash
python3 generator.py --start-date 2026-01-01 --end-date 2026-06-30
```

### 3. Target a Specific Repository
Specify the target repository folder using `--path`:

```bash
python3 generator.py --path /path/to/your/repo --start-date 2026-05-01 --end-date 2026-08-31
```

### 4. Restrict to a Single File (Optional)
If you prefer all commits to target a single log file instead of rotating files:

```bash
python3 generator.py --single-file activity_log.txt --start-date 2026-07-01 --end-date 2026-10-18
```

### 5. Push to GitHub
After generation, push to your remote branch:

```bash
git push origin main
```

---

## CLI Options

| Option | Type | Default | Description |
|---|---|---|---|
| `--start-date` | `YYYY-MM-DD` | `90 days ago` | Target commit start date |
| `--end-date` | `YYYY-MM-DD` | `Today` | Target commit end date |
| `--min-commits` | `int` | `2` | Minimum commits per active day |
| `--max-commits` | `int` | `5` | Maximum commits per active day |
| `--include-weekends` | `flag` | `False` | Include Saturday & Sunday (default: weekdays only) |
| `--single-file` | `str` | `None` | Restrict all commits to a single file path |
| `--dry-run` | `flag` | `False` | Preview commit plan without writing changes |
| `--path` | `str` | `.` | Target Git repository directory |

---

## Running Tests

Execute the automated test suite using `unittest`:

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

Or using `pytest`:

```bash
pip install -r requirements-dev.txt
pytest
```

---

## Disclaimer

This project is created for developer testing, simulation of Git contribution charts, and educational automation workflows. Please use responsibly on repositories you own or manage.

---

## License

This project is licensed under the [MIT License](LICENSE).
