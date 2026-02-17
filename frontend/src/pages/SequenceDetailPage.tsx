import { useState } from "react";
import { useParams } from "react-router-dom";
import { useSequence } from "../hooks/useSequences";
import type { ShotStatus } from "../api/types";
import { SHOT_STATUSES } from "../api/types";
import ShotTable from "../components/ShotTable";
import StatusPipeline from "../components/StatusPipeline";

export default function SequenceDetailPage() {
  const { id } = useParams<{ id: string }>();
  const { data: sequence, isLoading, error } = useSequence(Number(id));
  const [filter, setFilter] = useState<ShotStatus | null>(null);

  if (isLoading) {
    return (
      <div className="loading">
        <div className="spinner" />
        Loading sequence...
      </div>
    );
  }

  if (error || !sequence) {
    return <div className="error-state">Failed to load sequence.</div>;
  }

  const filteredShots = filter
    ? sequence.shots.filter((s) => s.status === filter)
    : sequence.shots;

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">{sequence.code}</h1>
        {sequence.description && (
          <p className="page-subtitle">{sequence.description}</p>
        )}
      </div>

      <div className="section">
        <div className="section-title">Shot Status Distribution</div>
        <StatusPipeline shots={sequence.shots} />
      </div>

      <div className="section">
        <div className="section-title">Shots</div>
        <div className="filter-chips">
          <button
            className={`filter-chip ${filter === null ? "filter-chip--active" : ""}`}
            onClick={() => setFilter(null)}
          >
            All ({sequence.shots.length})
          </button>
          {SHOT_STATUSES.map((status) => {
            const count = sequence.shots.filter(
              (s) => s.status === status,
            ).length;
            if (count === 0) return null;
            return (
              <button
                key={status}
                className={`filter-chip ${filter === status ? "filter-chip--active" : ""}`}
                onClick={() => setFilter(filter === status ? null : status)}
              >
                {status.replace("_", " ")} ({count})
              </button>
            );
          })}
        </div>
        <ShotTable shots={filteredShots} />
      </div>
    </div>
  );
}
