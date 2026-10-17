"""Constants, file targets, and Conventional Commit message templates."""

APP_NAME = "GitHub Activity & Contribution Generator"
VERSION = "1.1.0"

# Target files categorized by domain
FILE_TARGETS = {
    "code": [
        "src/utils.py",
        "src/validators.py",
        "src/helpers.py",
        "src/cache.py",
        "src/formatter.py",
    ],
    "docs": [
        "docs/api_reference.md",
        "docs/architecture.md",
        "docs/setup_guide.md",
        "CHANGELOG.md",
    ],
    "tests": [
        "tests/test_utils.py",
        "tests/test_validators.py",
        "tests/test_cache.py",
        "tests/test_formatter.py",
    ],
    "config": [
        "config/settings.json",
        "config/pipeline_config.json",
        "scripts/health_check.sh",
    ],
}

# Domain-specific Conventional Commit messages
COMMIT_TEMPLATES = {
    "code": [
        ("src/utils.py", "feat(utils): add exponential backoff retry handler"),
        ("src/utils.py", "refactor(utils): optimize string chunking memory footprint"),
        ("src/utils.py", "fix(utils): handle zero-division edge case in metrics computation"),
        ("src/validators.py", "feat(validators): add schema validator for payload models"),
        ("src/validators.py", "fix(validators): sanitize unicode control characters in input"),
        ("src/validators.py", "refactor(validators): compile regex patterns once at module load"),
        ("src/helpers.py", "feat(helpers): implement thread-safe memoization wrapper"),
        ("src/helpers.py", "refactor(helpers): streamline dictionary flattening helper"),
        ("src/cache.py", "feat(cache): add LRU eviction policy with configurable TTL"),
        ("src/cache.py", "fix(cache): prevent race condition during cache invalidation"),
        ("src/formatter.py", "feat(formatter): add ISO-8601 duration parser and formatter"),
        ("src/formatter.py", "perf(formatter): replace regex substitution with string partition"),
    ],
    "docs": [
        ("docs/api_reference.md", "docs(api): document pagination parameters and error codes"),
        ("docs/api_reference.md", "docs(api): add curl and python code samples for endpoints"),
        ("docs/architecture.md", "docs(arch): update sequence flow for background worker tasks"),
        ("docs/architecture.md", "docs(arch): document cache hierarchy and fallback paths"),
        ("docs/setup_guide.md", "docs(setup): clarify python virtual environment configuration"),
        ("docs/setup_guide.md", "docs(setup): add troubleshooting tips for local permissions"),
        ("CHANGELOG.md", "docs(changelog): record patch updates and bugfix summary"),
        ("CHANGELOG.md", "docs(changelog): update release notes for v1.1 milestone"),
    ],
    "tests": [
        ("tests/test_utils.py", "test(utils): add unit tests for exponential backoff edge cases"),
        ("tests/test_utils.py", "test(utils): verify exception propagation on retry exhaustion"),
        ("tests/test_validators.py", "test(validators): assert validation passes on valid unicode"),
        ("tests/test_validators.py", "test(validators): assert type error on null payload values"),
        ("tests/test_cache.py", "test(cache): verify TTL expiration under mock clock"),
        ("tests/test_cache.py", "test(cache): test thread safety across concurrent readers"),
        ("tests/test_formatter.py", "test(formatter): add regression assertions for duration parser"),
    ],
    "config": [
        ("config/settings.json", "chore(config): adjust default connection pool size and timeouts"),
        ("config/settings.json", "chore(config): add retry threshold parameters for worker tasks"),
        ("config/pipeline_config.json", "ci(config): tune worker concurrency limits"),
        ("scripts/health_check.sh", "chore(scripts): add curl probe for internal health endpoint"),
    ],
}

DEFAULT_WORK_HOURS = (9, 21)
DEFAULT_CHANCE_ACTIVE = 0.88
