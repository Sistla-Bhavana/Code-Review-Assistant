"""
AI Code Review Assistant — Flask backend

This is the main entry point. It exposes one endpoint:
POST /review  -> takes a code diff, returns AI-generated review comments
                 with a confidence/severity rating per comment.

Run locally with:
    python app.py
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import time

from github_client import fetch_pr_diff
from review import review_diff
from stats import log_review, get_stats

app = Flask(__name__)
CORS(app)  # allows the React frontend (running on a different port) to call this API


@app.route("/health", methods=["GET"])
def health():
    """Simple check to confirm the server is running."""
    return jsonify({"status": "ok"})


@app.route("/stats", methods=["GET"])
def stats():
    """Returns aggregate stats (avg response time, avg issues per review) across all logged runs."""
    return jsonify(get_stats())


@app.route("/review", methods=["POST"])
def review():
    """
    Accepts JSON body in one of two shapes:
      1) {"pr_url": "https://github.com/owner/repo/pull/123"}
      2) {"diff": "<raw diff text pasted directly>"}

    Returns:
      {
        "comments": [
          {
            "file": "app.py",
            "line": 42,
            "issue": "Possible null reference if `user` is None here.",
            "severity": "must-fix",       # "must-fix" or "suggestion"
            "confidence": "high"          # "high", "medium", or "low"
          },
          ...
        ]
      }
    """
    data = request.get_json(force=True)

    if not data or ("pr_url" not in data and "diff" not in data):
        return jsonify({"error": "Provide either 'pr_url' or 'diff' in the request body."}), 400

    try:
        start_time = time.time()

        if "pr_url" in data:
            diff_text = fetch_pr_diff(data["pr_url"])
        else:
            diff_text = data["diff"]

        if not diff_text.strip():
            return jsonify({"error": "No diff content found."}), 400

        result = review_diff(diff_text)

        elapsed = time.time() - start_time
        log_review(elapsed, result.get("comments", []))

        return jsonify(result)

    except Exception as e:
        # In a real production app we'd log this properly; for now, surface it clearly.
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
