# Code-Review-Assistant

An AI-powered code review assistant that analyzes GitHub Pull Requests and raw code diffs, identifies potential issues, and provides actionable review comments with confidence levels.

Built with **React, Flask, Python, and Google Gemini**, the application is designed to help developers identify bugs, code-quality issues, and improvement opportunities faster.

---

## 🚀 Overview

Code Review Assistant simplifies the code review process by automatically analyzing code changes and generating structured review feedback.

The system evaluates code changes and categorizes findings based on their importance, helping developers distinguish between:

- 🔴 Must-fix bugs
- 🟠 Potential issues
- 🟢 Code-quality improvements
- 🔵 Stylistic suggestions

Each review comment is also assigned a confidence level:

**High | Medium | Low**

This allows developers to focus their attention on the most important findings first.

---

## ✨ Key Features

### 🔍 AI-Powered Code Analysis
Analyzes code changes and identifies potential bugs, issues, and improvement opportunities.

### 🐙 GitHub Integration
Supports reviewing GitHub Pull Requests and retrieving code changes for analysis.

### 📄 Raw Diff Analysis
Allows developers to provide raw Git diffs for quick code reviews without requiring a GitHub Pull Request.

### 🎯 Confidence-Based Findings
Each generated review comment is categorized as:

- **High Confidence** – Strong evidence of a real issue
- **Medium Confidence** – Likely issue requiring developer verification
- **Low Confidence** – Possible improvement or minor concern

### 🐞 Bug vs. Suggestion Classification
Separates critical issues from optional stylistic or quality improvements.

### 🤖 Google Gemini Integration
Uses Google's Gemini models to generate intelligent code-review feedback.

### 🧪 Mock Mode
The application includes a mock/demo mode so the interface can be explored without configuring an API key.

### 💻 Modern Web Interface
Responsive React-based frontend designed for a clean and intuitive developer experience.

---

## 🛠️ Tech Stack

### Frontend

- React.js
- JavaScript
- HTML5
- CSS3
- Vite

### Backend

- Python
- Flask
- REST APIs

### AI

- Google Gemini API

### Development Tools

- Git
- GitHub
- VS Code

---

## 🏗️ Project Architecture

```text
Code-Review-Assistant/
│
├── backend/
│   ├── app.py
│   ├── github_client.py
│   ├── review.py
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.js
│
├── .gitignore
└── README.md

#🔄 How It Works
GitHub Pull Request / Raw Diff
              │
              ▼
        React Frontend
              │
              ▼
        Flask REST API
              │
              ▼
      Code Analysis Engine
              │
              ▼
        Google Gemini AI
              │
              ▼
      Structured Review
              │
              ▼
 ┌──────────────────────────┐
 │ Bug / Issue              │
 │ Confidence Level         │
 │ Explanation              │
 │ Suggested Improvement    │
 └──────────────────────────┘

 Getting Started
1. Clone the Repository
git clone https://github.com/Sistla-Bhavana/Code-Review-Assistant.git

Navigate into the project:

cd Code-Review-Assistant
🔧 Backend Setup

Navigate to the backend directory:

cd backend

Create a virtual environment:

python -m venv venv

Activate the environment on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GEMINI_API_KEY=your_api_key_here

Important: Never commit your .env file or API keys to GitHub.

Start the Flask server:

python app.py
🎨 Frontend Setup

Open another terminal and navigate to the frontend:

cd frontend

Install dependencies:

npm install

Start the development server:

npm run dev

The frontend will be available through the local URL displayed by Vite.

🧪 Demo / Mock Mode

The application can be used in mock mode to explore the interface without configuring an AI API key.

This makes it easy for developers, recruiters, and clients to evaluate the application locally.

📌 Example Review Output

A typical review finding can contain:

Issue:
Potential null reference detected.

Type:
Bug

Confidence:
High

Explanation:
The variable may be accessed before being initialized,
which could result in a runtime error.

Recommendation:
Validate the variable before accessing its properties.
🎯 Use Cases

Code Review Assistant can be useful for:

Individual developers
Software development teams
Code quality analysis
Pull Request reviews
Learning and improving coding practices
Identifying potential bugs
Automated development workflows
🔮 Future Improvements

Planned improvements include:

Support for additional AI models
Automated GitHub Pull Request comments
Multi-language code analysis
Code quality scoring
Security vulnerability detection
Custom review rules
Review history and analytics
CI/CD integration
Authentication and user accounts
🔐 Security

API keys and sensitive credentials should always be stored in environment variables.

The repository intentionally excludes environment files using .gitignore.

Never expose API keys, GitHub tokens, or other credentials in source code or public repositories.
