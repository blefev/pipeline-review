import { useState } from "react";
import type { ReviewCreate, ReviewStatus } from "../api/types";
import { useCreateReview } from "../hooks/useReviews";

interface Props {
  shotId: number;
}

export default function ReviewForm({ shotId }: Props) {
  const [author, setAuthor] = useState("");
  const [status, setStatus] = useState<ReviewStatus>("note");
  const [body, setBody] = useState("");
  const [department, setDepartment] = useState("");

  const createReview = useCreateReview(shotId);

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (!author.trim() || !body.trim()) return;

    const review: ReviewCreate = {
      author: author.trim(),
      status,
      body: body.trim(),
    };
    if (department.trim()) {
      review.department = department.trim();
    }

    createReview.mutate(review, {
      onSuccess: () => {
        setBody("");
      },
    });
  }

  return (
    <form onSubmit={handleSubmit}>
      <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
        <div className="form-group">
          <label className="form-label">Author</label>
          <input
            className="form-input"
            value={author}
            onChange={(e) => setAuthor(e.target.value)}
            placeholder="Your name"
            required
          />
        </div>
        <div className="form-group">
          <label className="form-label">Department</label>
          <input
            className="form-input"
            value={department}
            onChange={(e) => setDepartment(e.target.value)}
            placeholder="e.g. lighting, comp"
          />
        </div>
      </div>
      <div className="form-group">
        <label className="form-label">Status</label>
        <select
          className="form-select"
          value={status}
          onChange={(e) => setStatus(e.target.value as ReviewStatus)}
        >
          <option value="note">Note</option>
          <option value="approved">Approved</option>
          <option value="needs_revision">Needs Revision</option>
        </select>
      </div>
      <div className="form-group">
        <label className="form-label">Review Notes</label>
        <textarea
          className="form-textarea"
          value={body}
          onChange={(e) => setBody(e.target.value)}
          placeholder="Enter review feedback..."
          required
        />
      </div>
      <button
        type="submit"
        className="btn btn--primary"
        disabled={createReview.isPending || !author.trim() || !body.trim()}
      >
        {createReview.isPending ? "Submitting..." : "Submit Review"}
      </button>
    </form>
  );
}
