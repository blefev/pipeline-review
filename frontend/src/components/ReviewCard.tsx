import type { Review } from "../api/types";

interface Props {
  review: Review;
}

const STATUS_LABELS: Record<string, string> = {
  approved: "Approved",
  needs_revision: "Needs Revision",
  note: "Note",
};

export default function ReviewCard({ review }: Props) {
  return (
    <div className="review-card">
      <div className="review-card__header">
        <span className="review-card__author">{review.author}</span>
        <div className="review-card__meta">
          {review.department && (
            <span className="department-tag">{review.department}</span>
          )}
          <span>{STATUS_LABELS[review.status] ?? review.status}</span>
          <span>{new Date(review.created_at).toLocaleString()}</span>
        </div>
      </div>
      <div className="review-card__body">{review.body}</div>
    </div>
  );
}
