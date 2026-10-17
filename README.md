# GitHub Activity & Contribution Generator

A Python CLI tool to customize, backdate, and simulate Git commit histories and GitHub contribution activity graphs.

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

---

## Features

- **Custom Date Ranges**: Generate commits across any historical date range (`--start-date`, `--end-date`).
- **Professional Weekday Scheduling**: Automatically filters out weekends by default to maintain natural developer work patterns.
- **Natural Commit Volumes**: Configurable daily frequency bounds (`--min-commits`, `--max-commits`) preventing obvious robotic spikes.
- **Business Hours Distribution**: Commits are generated during realistic daylight and evening hours with randomized spacing.
- **Dry-Run Preview**: Preview exact dates, frequencies, and messages before creating any Git commits.
- **Zero External Dependencies**: Built entirely using Python's standard library.

---

## Installation

Clone the repository:

```bash
git clone https://github.com/hamzach9410/github-activity-generator.git
cd github-activity-generator
```

No external pip packages required. Runs on Python 3.8+.

---

## Quickstart

### 1. Preview with Dry-Run
Preview the schedule without touching your Git repository:

```bash
python3 generator.py --dry-run
```

### 2. Generate Commits for the Past 3 Months
```bash
python3 generator.py --start-date 2026-07-01 --end-date 2026-10-18
```

### 3. Customize Daily Commit Frequency
```bash
python3 generator.py --min-commits 1 --max-commits 4 --start-date 2026-01-01 --end-date 2026-06-30
```

### 4. Push to Remote
After generation, publish to your GitHub repository:

```bash
git push origin main
```

---

## CLI Options

| Flag | Type | Default | Description |
|---|---|---|---|
| `--start-date` | `YYYY-MM-DD` | 180 days ago | Beginning of target commit range |
| `--end-date` | `YYYY-MM-DD` | Today | End of target commit range |
| `--min-commits` | `int` | `2` | Minimum commits on active days |
| `--max-commits` | `int` | `5` | Maximum commits on active days |
| `--include-weekends`| `flag` | `False` | Includes Saturday & Sunday (default: weekdays only) |
| `--dry-run` | `flag` | `False` | Previews planned schedule without making commits |
| `--path` | `str` | `.` | Target repository directory |

---

## Disclaimer

This utility is designed for Git workflow simulation, integration testing, and educational graph customization. Use responsibly on repositories you own or manage.

---

## License

This project is licensed under the [MIT License](LICENSE).
