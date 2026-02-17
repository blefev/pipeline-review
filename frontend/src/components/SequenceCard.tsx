import { Link } from "react-router-dom";
import type { Sequence } from "../api/types";

interface Props {
  sequence: Sequence;
}

export default function SequenceCard({ sequence }: Props) {
  return (
    <Link
      to={`/sequences/${sequence.id}`}
      style={{ textDecoration: "none", color: "inherit" }}
    >
      <div className="card">
        <div className="card-title">{sequence.code}</div>
        {sequence.description && (
          <div className="card-meta">{sequence.description}</div>
        )}
      </div>
    </Link>
  );
}
