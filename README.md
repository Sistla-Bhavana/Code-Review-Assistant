# AI Code Review Assistant

An AI-powered code review tool that reviews GitHub pull requests (or raw diffs) and returns feedback tagged with **confidence ratings** — so instead of treating every AI comment as equally trustworthy, you can immediately see what's a high-confidence bug versus a low-confidence stylistic suggestion.

## Why this exists

Most AI code review tools present every comment with the same authority, whether it's catching a genuine null-reference bug or just expressing a style opinion. This tool separates **"must-fix" issues from "suggestions"**, and rates its own **confidence** (high / medium / low) on each one — a small but important step toward AI tools that communicate what they actually know versus what they're guessing at.

## Features

- Review any public GitHub PR by URL, or paste a raw diff directly
- Comments are split into **Must Fix** (bugs, security issues, correctness problems) and **Suggestions** (style, naming, minor improvements)
- Each comment includes a **confidence rating** so you know how much to trust it
- Runs in **mock mode** automatically if no API key is set — the whole app is testable end-to-end with zero setup cost

## Tech stack

- **Backend:** Python, Flask, Flask-CORS
- **Frontend:** React, Vite
- **AI:** Google Gemini API (`gemini-1.5-flash`)
- **Data:** GitHub REST API (public PR diffs, no auth required)

## Architecture

```
React (Vite)  →  Flask API  →  GitHub API (fetch PR diff)
                             →  Gemini API (generate review)
```

The AI call is isolated behind a single function (`call_llm` in `backend/review.py`), so swapping providers only requires changing one file.

## Running locally

**Backend:**
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Runs at `http://localhost:5000`.

**Frontend** (in a separate terminal):
```bash
cd frontend
npm install
npm run dev
```
Runs at `http://localhost:5173`.

### Enabling real AI reviews (optional)

By default the app runs in mock mode (no API key needed) so you can try the full flow immediately. To get real, PR-specific reviews:

1. Get a free API key from [Google AI Studio](https://aistudio.google.com)
2. Create a file `backend/.env` containing:
   ```
   GEMINI_API_KEY=your-key-here
   ```
3. Restart the backend — it automatically detects the key and switches out of mock mode.

## Example

Try it on a small real PR: `https://github.com/docsifyjs/docsify-cli/pull/105`

## Project structure

```
code-review-assistant/
├── backend/
│   ├── app.py            # Flask routes
│   ├── github_client.py  # Fetches PR diffs from GitHub's API
│   ├── review.py          # Prompt + AI call (the only file needed to swap providers)
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx        # UI: input, results, confidence badges
    │   └── main.jsx
    └── package.json
```

## Roadmap

- [ ] Deploy backend (Render) and frontend (Vercel)
- [ ] Add a review-history log so past reviews are searchable
- [ ] Support private repos via a GitHub personal access token
