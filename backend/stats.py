"""
Lightweight, dependency-free stats logging.

Every /review call appends one row to a local CSV: timestamp, elapsed time,
issue counts by severity. No database needed — this is just for collecting
real numbers (average response time, average issues per PR) instead of
guessing them, so you can quote actual measured stats rather than estimates.
"""

import csv
import os
import time
from datetime import datetime

LOG_PATH = os.path.join(os.path.dirname(__file__), "review_stats.csv")

FIELDNAMES = ["timestamp", "elapsed_seconds", "total_issues", "must_fix_count", "suggestion_count"]


def log_review(elapsed_seconds: float, comments: list):
    """Appends one row for this review run."""
    must_fix_count = sum(1 for c in comments if c.get("severity") == "must-fix")
    suggestion_count = sum(1 for c in comments if c.get("severity") == "suggestion")

    file_exists = os.path.isfile(LOG_PATH)
    with open(LOG_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not file_exists:
            writer.writeheader()
        writer.writerow(
            {
                "timestamp": datetime.utcnow().isoformat(),
                "elapsed_seconds": round(elapsed_seconds, 2),
                "total_issues": len(comments),
                "must_fix_count": must_fix_count,
                "suggestion_count": suggestion_count,
            }
        )


def get_stats() -> dict:
    """Reads the log and returns aggregate stats across all runs so far."""
    if not os.path.isfile(LOG_PATH):
        return {"runs_logged": 0, "message": "No reviews logged yet. Run a few /review calls first."}

    with open(LOG_PATH, "r", newline="") as f:
        rows = list(csv.DictReader(f))

    if not rows:
        return {"runs_logged": 0, "message": "No reviews logged yet."}

    n = len(rows)
    avg_elapsed = sum(float(r["elapsed_seconds"]) for r in rows) / n
    avg_issues = sum(int(r["total_issues"]) for r in rows) / n
    avg_must_fix = sum(int(r["must_fix_count"]) for r in rows) / n
    avg_suggestion = sum(int(r["suggestion_count"]) for r in rows) / n

    return {
        "runs_logged": n,
        "avg_response_time_seconds": round(avg_elapsed, 2),
        "avg_issues_per_review": round(avg_issues, 1),
        "avg_must_fix_per_review": round(avg_must_fix, 1),
        "avg_suggestions_per_review": round(avg_suggestion, 1),
    }
