import { useParams } from "react-router-dom";
import { useShow } from "../hooks/useShows";
import SequenceCard from "../components/SequenceCard";

export default function ShowDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: show, isLoading, error } = useShow(Number(id));

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner" />
        Loading show...
      </div>
    );
  }

  if (error || !show) {
    return <div className="error-state">Failed to load show.</div>;
  }

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">{show.title}</h1>
        <p className="page-subtitle">
          <span className="shot-code">{show.code}</span> &middot;{" "}
          {show.sequences.length} sequence{show.sequences.length !== 1 && "s"}
        </p>
      </div>

      {show.sequences.length === 0 ? (
        <div className="empty-state">
          No sequences yet. Seed the database to create demo data.
        </div>
      ) : (
        <div className="card-grid">
          {show.sequences.map((seq) => (
            <SequenceCard key={seq.id} sequence={seq} />
          ))}
        </div>
      )}
    </div>
  );
}
