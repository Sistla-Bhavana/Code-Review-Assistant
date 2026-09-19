"""
This is the ONLY file you'll need to touch once you get your Gemini API key.
Everything else (Flask routes, GitHub fetching) stays exactly the same.

Right now `call_llm()` runs in MOCK_MODE — it returns fake-but-realistic
review comments so you can build and test the whole app end-to-end
(backend + frontend) before wiring up a real AI provider.

When you're ready to go live:
  1. pip install google-generativeai
  2. Set MOCK_MODE = False below
  3. Fill in the real Gemini call in call_llm() (marked with TODO)
"""

import json
import os

from dotenv import load_dotenv

load_dotenv()  # reads GEMINI_API_KEY from a local .env file, if present

# If no key is found in the environment, we automatically fall back to mock
# mode instead of crashing — this way the app still runs for anyone who
# hasn't set up a key yet (e.g. during early development or a demo).
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
MOCK_MODE = not GEMINI_API_KEY

if not MOCK_MODE:
    import google.generativeai as genai

    genai.configure(api_key=GEMINI_API_KEY)
    _model = genai.GenerativeModel("gemini-flash-latest")


def call_llm(prompt: str) -> str:
    """
    Sends a prompt to the AI model and returns its raw text response.
    This is the single seam between your app and whichever AI provider you use.

    Runs in mock mode automatically if GEMINI_API_KEY isn't set in the
    environment — no code changes needed to switch between the two, just
    add or remove the key from your .env file.
    """
    if MOCK_MODE:
        return _mock_response()

    response = _model.generate_content(prompt)
    return response.text


def _mock_response() -> str:
    """A realistic fake response, shaped exactly like we expect the real LLM to reply."""
    return json.dumps(
        {
            "comments": [
                {
                    "file": "app.py",
                    "line": 42,
                    "issue": "`user` could be None here if the lookup fails, causing an AttributeError.",
                    "severity": "must-fix",
                    "confidence": "high",
                },
                {
                    "file": "app.py",
                    "line": 58,
                    "issue": "Variable name `d` is unclear — consider renaming to something descriptive like `diff_text`.",
                    "severity": "suggestion",
                    "confidence": "medium",
                },
                {
                    "file": "utils.py",
                    "line": 12,
                    "issue": "This loop re-computes the same value on every iteration — consider moving it outside the loop.",
                    "severity": "suggestion",
                    "confidence": "low",
                },
            ]
        }
    )


def build_review_prompt(diff_text: str) -> str:
    """
    Builds the instruction we send to the AI model.
    Asks explicitly for confidence + severity per comment, and for strict JSON
    output so the frontend can render it reliably.
    """
    return f"""You are a senior software engineer reviewing a code diff.

For each issue you find, output an entry with:
- file: the filename
- line: the approximate line number
- issue: a clear, specific description of the problem
- severity: "must-fix" (bugs, security issues, correctness problems) or "suggestion" (style, naming, minor improvements)
- confidence: "high", "medium", or "low" — how sure you are this is a real issue, not a stylistic opinion

Be honest about confidence. Don't inflate "suggestion" items to "must-fix", and don't mark something "high confidence" unless you're genuinely certain it's a bug.

Respond with ONLY valid JSON in this exact shape, no other text:
{{"comments": [{{"file": "...", "line": 0, "issue": "...", "severity": "...", "confidence": "..."}}]}}

Diff to review:
{diff_text}
"""


def review_diff(diff_text: str) -> dict:
    """
    Main entry point used by app.py. Builds the prompt, calls the LLM,
    parses the JSON response, and returns it as a Python dict.
    """
    prompt = build_review_prompt(diff_text)
    raw_response = call_llm(prompt)

    # Gemini sometimes wraps JSON in markdown code fences (```json ... ```)
    # even when told not to — strip those off before parsing if present.
    cleaned = raw_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
        cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        # If the model wraps the JSON in markdown fences or adds stray text,
        # this is where you'd add cleanup logic. For now, surface the raw text
        # so it's easy to debug what the model actually returned.
        raise ValueError(f"Could not parse AI response as JSON. Raw response:\n{cleaned}")
