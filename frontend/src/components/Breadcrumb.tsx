import { Link, useMatches } from "react-router-dom";

interface CrumbData {
  crumb?: { label: string; to?: string };
}

export default function Breadcrumb() {
  const matches = useMatches();

  const crumbs = matches
    .filter((m) => (m.data as CrumbData)?.crumb)
    .map((m) => (m.data as CrumbData).crumb!);

  if (crumbs.length === 0) {
    return <nav className="breadcrumb" />;
  }

  return (
    <nav className="breadcrumb">
      <Link to="/">Shows</Link>
      {crumbs.map((crumb, i) => (
        <span key={i}>
          <span className="breadcrumb-separator">/</span>
          {crumb.to ? (
            <Link to={crumb.to}>{crumb.label}</Link>
          ) : (
            <span>{crumb.label}</span>
          )}
        </span>
      ))}
    </nav>
  );
}
