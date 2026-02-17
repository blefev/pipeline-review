import { useShows } from "../hooks/useShows";
import ShowCard from "../components/ShowCard";

export default function ShowListPage() {
  const { data: shows, isLoading, error } = useShows();

  return (
    <div>
      <div className="page-header">
        <h1 className="page-title">Shows</h1>
        <p className="page-subtitle">All active productions</p>
      </div>

      {isLoading && (
        <div className="loading">
          <div className="spinner" />
          Loading shows...
        </div>
      )}

      {error && (
        <div className="error-state">
          Failed to load shows. Is the API running?
        </div>
      )}

      {shows && shows.length === 0 && (
        <div className="empty-state">
          No shows yet. Click "Seed Database" to populate demo data.
        </div>
      )}

      {shows && shows.length > 0 && (
        <div className="card-grid">
          {shows.map((show) => (
            <ShowCard key={show.id} show={show} />
          ))}
        </div>
      )}
    </div>
  );
}
