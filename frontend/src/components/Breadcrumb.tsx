import { Link, useLocation } from "react-router-dom";

export default function Breadcrumb() {
  const { pathname } = useLocation();

  if (pathname === "/") {
    return <nav className="breadcrumb"><span>Shows</span></nav>;
  }

  const segments = pathname.split("/").filter(Boolean);
  const crumbs: { label: string; to: string }[] = [
    { label: "Shows", to: "/" },
  ];

  for (let i = 0; i < segments.length; i += 2) {
    const resource = segments[i];
    const id = segments[i + 1];
    if (resource && id) {
      const label =
        resource === "shows"
          ? `Show ${id}`
          : resource === "sequences"
            ? `Sequence ${id}`
            : resource === "shots"
              ? `Shot ${id}`
              : id;
      crumbs.push({ label, to: `/${resource}/${id}` });
    } else if (resource === "search") {
      crumbs.push({ label: "Search", to: "/search" });
    }
  }

  return (
    <nav className="breadcrumb">
      {crumbs.map((crumb, i) => (
        <span key={crumb.to}>
          {i > 0 && <span className="breadcrumb-separator">/</span>}
          {i === crumbs.length - 1 ? (
            <span>{crumb.label}</span>
          ) : (
            <Link to={crumb.to}>{crumb.label}</Link>
          )}
        </span>
      ))}
    </nav>
  );
}
