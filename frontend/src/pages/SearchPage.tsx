import { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useSearchReviews } from "../hooks/useSearch";

function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);

  useEffect(() => {
    const timer = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);

  return debounced;
}

export default function SearchPage() {
  const [input, setInput] = useState("");
  const query = useDebounce(input.trim(), 300);
  const { data: results, isLoading, error } = useSearchReviews(query);

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Search Reviews</h1>
        <p className="page-subtitle">
          Full-text search across all review notes
        </p>
      </div>

      <div className="search-input-wrapper">
        <span className="search-icon">&#128269;</span>
        <input
          className="search-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder='Search reviews... e.g. "lighting bounces"'
        />
      </div>

      {query.length === 0 && (
        <div className="empty-state">
          Type a search query to find reviews by content.
        </div>
      )}

      {isLoading && query.length > 0 && (
        <div className="loading">
          <div className="spinner" />
          Searching...
        </div>
      )}

      {error && <div className="error-state">Search failed.</div>}

      {results && results.length === 0 && query.length > 0 && (
        <div className="empty-state">
          No reviews found for "{query}".
        </div>
      )}

      {results && results.length > 0 && (
        <div className="review-timeline">
          {results.map((result) => (
            <div key={result.id} className="review-card">
              <div className="review-card__header">
                <span className="review-card__author">{result.author}</span>
                <div className="review-card__meta">
                  {result.department && (
                    <span className="department-tag">{result.department}</span>
                  )}
                  <span className="search-score">
                    score: {result.score.toFixed(2)}
                  </span>
                  <Link to={`/shots/${result.shot_id}`}>
                    View Shot
                  </Link>
                </div>
              </div>
              <div className="review-card__body">{result.body}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
