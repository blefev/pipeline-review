import type { Shot, ShotStatus } from "../api/types";
import { SHOT_STATUSES } from "../api/types";

interface Props {
  shots: Shot[];
}

const STATUS_LABELS: Record<ShotStatus, string> = {
  pending: "Pending",
  in_progress: "In Progress",
  review: "Review",
  approved: "Approved",
  final: "Final",
};

export default function StatusPipeline({ shots }: Props) {
  const total = shots.length;
  if (total === 0) return null;

  const counts = SHOT_STATUSES.reduce(
    (acc, s) => {
      acc[s] = shots.filter((shot) => shot.status === s).length;
      return acc;
    },
    {} as Record<ShotStatus, number>,
  );

  return (
    <div>
      <div className="status-pipeline">
        {SHOT_STATUSES.map(
          (status) =>
            counts[status] > 0 && (
              <div
                key={status}
                className={`status-pipeline__segment status-pipeline__segment--${status}`}
                style={{ width: `${(counts[status] / total) * 100}%` }}
                title={`${STATUS_LABELS[status]}: ${counts[status]}`}
              />
            ),
        )}
      </div>
      <div className="status-pipeline-legend">
        {SHOT_STATUSES.map(
          (status) =>
            counts[status] > 0 && (
              <div key={status} className="status-pipeline-legend__item">
                <div
                  className="status-pipeline-legend__dot"
                  style={{
                    background: `var(--status-${status})`,
                  }}
                />
                <span>
                  {STATUS_LABELS[status]} ({counts[status]})
                </span>
              </div>
            ),
        )}
      </div>
    </div>
  );
}
