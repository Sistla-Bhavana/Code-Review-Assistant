"""
Handles pulling a diff from a GitHub Pull Request URL.

GitHub lets you fetch a PR's diff without authentication for public repos —
just by requesting the PR URL with a special Accept header.
"""

import re
import requests


def parse_pr_url(pr_url: str):
    """
    Turns 'https://github.com/owner/repo/pull/123' into ('owner', 'repo', '123').
    Raises ValueError if the URL doesn't look like a GitHub PR link.
    """
    match = re.match(r"https://github\.com/([^/]+)/([^/]+)/pull/(\d+)", pr_url.strip())
    if not match:
        raise ValueError(
            "That doesn't look like a GitHub PR URL. "
            "Expected format: https://github.com/owner/repo/pull/123"
        )
    owner, repo, pr_number = match.groups()
    return owner, repo, pr_number


def fetch_pr_diff(pr_url: str) -> str:
    """
    Fetches the raw diff text for a given GitHub PR URL.
    Works for public repos without needing a GitHub token.
    """
    owner, repo, pr_number = parse_pr_url(pr_url)

    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    headers = {"Accept": "application/vnd.github.v3.diff"}

    response = requests.get(api_url, headers=headers, timeout=15)

    if response.status_code == 404:
        raise ValueError("PR not found. Check the URL, or the repo may be private.")
    if response.status_code == 403:
        raise ValueError("GitHub rate limit hit. Try again in a bit, or use a smaller diff instead.")
    response.raise_for_status()

    return response.text
