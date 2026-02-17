import type { ShotStatus } from "../api/types";

interface Props {
  status: ShotStatus;
}

const LABELS: Record<ShotStatus, string> = {
  pending: "Pending",
  in_progress: "In Progress",
  review: "Review",
  approved: "Approved",
  final: "Final",
};

export default function ShotStatusBadge({ status }: Props) {
  return (
    <span className={`status-badge status-badge--${status}`}>
      {LABELS[status]}
    </span>
  );
}
