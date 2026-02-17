import { Link } from "react-router-dom";
import type { Show } from "../api/types";

interface Props {
  show: Show;
}

export default function ShowCard({ show }: Props) {
  return (
    <Link to={`/shows/${show.id}`} style={{ textDecoration: "none", color: "inherit" }}>
      <div className="card">
        <div className="card-title">{show.title}</div>
        <div className="card-code">{show.code}</div>
        <div className="card-meta">
          Status: {show.status} &middot;{" "}
          {new Date(show.created_at).toLocaleDateString()}
        </div>
      </div>
    </Link>
  );
}
