import React, { useState } from "react";

// Points at your local Flask server during development.
// Change this to your deployed Render URL once you deploy the backend.
const API_URL = "http://localhost:5000";

const SEVERITY_LABEL = {
  "must-fix": "Must Fix",
  suggestion: "Suggestion",
};

const CONFIDENCE_COLOR = {
  high: "#E5484D",
  medium: "#F5A623",
  low: "#6B7785",
};

export default function App() {
  const [mode, setMode] = useState("pr_url"); // "pr_url" or "diff"
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [comments, setComments] = useState(null);

  async function handleReview() {
    if (!input.trim()) {
      setError("Please enter a PR URL or paste a diff first.");
      return;
    }

    setLoading(true);
    setError(null);
    setComments(null);

    try {
      const body = mode === "pr_url" ? { pr_url: input } : { diff: input };

      const response = await fetch(`${API_URL}/review`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Something went wrong.");
      }

      setComments(data.comments || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  const mustFix = comments?.filter((c) => c.severity === "must-fix") || [];
  const suggestions = comments?.filter((c) => c.severity === "suggestion") || [];

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <h1 style={styles.title}>AI Code Review Assistant</h1>
        <p style={styles.subtitle}>
          Paste a GitHub PR URL or a raw diff. Every comment comes with a confidence rating —
          so you know what to trust and what to double-check yourself.
        </p>

        <div style={styles.toggleRow}>
          <button
            onClick={() => setMode("pr_url")}
            style={mode === "pr_url" ? styles.toggleActive : styles.toggle}
          >
            GitHub PR URL
          </button>
          <button
            onClick={() => setMode("diff")}
            style={mode === "diff" ? styles.toggleActive : styles.toggle}
          >
            Paste Diff
          </button>
        </div>

        {mode === "pr_url" ? (
          <input
            style={styles.input}
            placeholder="https://github.com/owner/repo/pull/123"
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        ) : (
          <textarea
            style={styles.textarea}
            placeholder="Paste your diff here..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
          />
        )}

        <button style={styles.submitButton} onClick={handleReview} disabled={loading}>
          {loading ? "Reviewing..." : "Review Code"}
        </button>

        {error && <div style={styles.error}>{error}</div>}

        {comments && (
          <div style={styles.results}>
            <ResultSection title={`Must Fix (${mustFix.length})`} items={mustFix} />
            <ResultSection title={`Suggestions (${suggestions.length})`} items={suggestions} />
          </div>
        )}
      </div>
    </div>
  );
}

function ResultSection({ title, items }) {
  if (items.length === 0) return null;
  return (
    <div style={{ marginBottom: "24px" }}>
      <h3 style={styles.sectionTitle}>{title}</h3>
      {items.map((c, i) => (
        <div key={i} style={styles.card}>
          <div style={styles.cardHeader}>
            <span style={styles.fileLabel}>
              {c.file}:{c.line}
            </span>
            <span style={{ ...styles.confidenceBadge, color: CONFIDENCE_COLOR[c.confidence] }}>
              {c.confidence} confidence
            </span>
          </div>
          <div style={styles.issueText}>{c.issue}</div>
        </div>
      ))}
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#0B0F14",
    color: "#E4E9EE",
    fontFamily: "'IBM Plex Sans', ui-sans-serif, system-ui, sans-serif",
    padding: "40px 20px",
  },
  container: { maxWidth: "700px", margin: "0 auto" },
  title: { fontSize: "26px", fontWeight: 700, marginBottom: "6px" },
  subtitle: { fontSize: "14px", color: "#9BA7B4", marginBottom: "24px", lineHeight: 1.5 },
  toggleRow: { display: "flex", gap: "8px", marginBottom: "12px" },
  toggle: {
    padding: "8px 14px",
    borderRadius: "6px",
    border: "1px solid #1F2833",
    background: "#131920",
    color: "#9BA7B4",
    cursor: "pointer",
  },
  toggleActive: {
    padding: "8px 14px",
    borderRadius: "6px",
    border: "1px solid #4FD8E8",
    background: "#132226",
    color: "#4FD8E8",
    cursor: "pointer",
  },
  input: {
    width: "100%",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #1F2833",
    background: "#131920",
    color: "#E4E9EE",
    fontSize: "14px",
    marginBottom: "14px",
    boxSizing: "border-box",
  },
  textarea: {
    width: "100%",
    minHeight: "160px",
    padding: "12px",
    borderRadius: "8px",
    border: "1px solid #1F2833",
    background: "#131920",
    color: "#E4E9EE",
    fontSize: "13px",
    fontFamily: "ui-monospace, monospace",
    marginBottom: "14px",
    boxSizing: "border-box",
    resize: "vertical",
  },
  submitButton: {
    padding: "12px 20px",
    borderRadius: "8px",
    border: "none",
    background: "#4FD8E8",
    color: "#0B0F14",
    fontWeight: 600,
    cursor: "pointer",
    fontSize: "14px",
  },
  error: {
    marginTop: "14px",
    padding: "10px 14px",
    borderRadius: "6px",
    background: "#2A1518",
    border: "1px solid #E5484D44",
    color: "#E5484D",
    fontSize: "13px",
  },
  results: { marginTop: "30px" },
  sectionTitle: { fontSize: "15px", marginBottom: "10px", color: "#C7D0D8" },
  card: {
    background: "#131920",
    border: "1px solid #1F2833",
    borderRadius: "8px",
    padding: "12px 14px",
    marginBottom: "8px",
  },
  cardHeader: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "6px",
  },
  fileLabel: { fontFamily: "ui-monospace, monospace", fontSize: "12px", color: "#6B7785" },
  confidenceBadge: { fontSize: "11px", fontWeight: 600, textTransform: "uppercase" },
  issueText: { fontSize: "13.5px", color: "#C7D0D8", lineHeight: 1.5 },
};
