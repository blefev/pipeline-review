import { Link } from "react-router-dom";
import type { Shot } from "../api/types";
import ShotStatusBadge from "./ShotStatusBadge";

interface Props {
  shots: Shot[];
}

export default function ShotTable({ shots }: Props) {
  if (shots.length === 0) {
    return <div className="empty-state">No shots in this sequence.</div>;
  }

  return (
    <table className="data-table">
      <thead>
        <tr>
          <th>Code</th>
          <th>Status</th>
          <th>Assigned To</th>
          <th>Frames</th>
          <th>Updated</th>
        </tr>
      </thead>
      <tbody>
        {shots.map((shot) => (
          <tr key={shot.id}>
            <td>
              <Link to={`/shots/${shot.id}`} className="shot-code">
                {shot.code}
              </Link>
            </td>
            <td>
              <ShotStatusBadge status={shot.status} />
            </td>
            <td>{shot.assigned_to ?? "—"}</td>
            <td className="shot-code">
              {shot.frame_start}–{shot.frame_end}
            </td>
            <td>{new Date(shot.updated_at).toLocaleDateString()}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}
