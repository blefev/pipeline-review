import { useParams } from "react-router-dom";
import { useShot, useUpdateShot } from "../hooks/useShots";
import type { ShotStatus } from "../api/types";
import { SHOT_STATUSES } from "../api/types";
import ShotStatusBadge from "../components/ShotStatusBadge";
import ReviewCard from "../components/ReviewCard";
import ReviewForm from "../components/ReviewForm";

export default function ShotDetailPage() {
  const { id } = useParams<{ id: string }>();
  const shotId = Number(id);
  const { data: shot, isLoading, error } = useShot(shotId);
  const updateShot = useUpdateShot(shotId);

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner" />
        Loading shot...
      </div>
    );
  }

  if (error || !shot) {
    return <div className="error-state">Failed to load shot.</div>;
  }

  function handleStatusChange(e: React.ChangeEvent<HTMLSelectElement>) {
    updateShot.mutate({ status: e.target.value as ShotStatus });
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">
          <span className="shot-code">{shot.code}</span>
        </h1>
      </div>

      <div className="meta-grid">
        <div className="meta-item">
          <div className="meta-item__label">Status</div>
          <div className="meta-item__value">
            <select
              className="form-select"
              value={shot.status}
              onChange={handleStatusChange}
              disabled={updateShot.isPending}
              style={{ marginTop: 4 }}
            >
              {SHOT_STATUSES.map((s) => (
                <option key={s} value={s}>
                  {s.replace("_", " ")}
                </option>
              ))}
            </select>
          </div>
        </div>
        <div className="meta-item">
          <div className="meta-item__label">Current</div>
          <div className="meta-item__value">
            <ShotStatusBadge status={shot.status} />
          </div>
        </div>
        <div className="meta-item">
          <div className="meta-item__label">Assigned To</div>
          <div className="meta-item__value">
            {shot.assigned_to ?? "Unassigned"}
          </div>
        </div>
        <div className="meta-item">
          <div className="meta-item__label">Frame Range</div>
          <div className="meta-item__value" style={{ fontFamily: "var(--font-mono)" }}>
            {shot.frame_start}–{shot.frame_end}
          </div>
        </div>
        <div className="meta-item">
          <div className="meta-item__label">Updated</div>
          <div className="meta-item__value" style={{ fontSize: 14 }}>
            {new Date(shot.updated_at).toLocaleString()}
          </div>
        </div>
      </div>

      <div className="section">
        <div className="section-title">
          Reviews ({shot.reviews.length})
        </div>
        <div className="review-timeline">
          {shot.reviews.length === 0 ? (
            <div className="empty-state">No reviews yet.</div>
          ) : (
            [...shot.reviews]
              .sort(
                (a, b) =>
                  new Date(b.created_at).getTime() -
                  new Date(a.created_at).getTime(),
              )
              .map((review) => (
                <ReviewCard key={review.id} review={review} />
              ))
          )}
        </div>
      </div>

      <div className="section">
        <div className="section-title">Add Review</div>
        <ReviewForm shotId={shotId} />
      </div>
    </div>
  );
}
