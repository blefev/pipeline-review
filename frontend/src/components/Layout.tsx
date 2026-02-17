import { Outlet } from "react-router-dom";

export default function Layout() {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">Pipeline Review</div>
        <nav>
          <ul className="sidebar-nav">
            <li><a href="/">Shows</a></li>
            <li><a href="/search">Search</a></li>
          </ul>
        </nav>
      </aside>
      <div className="main-area">
        <header className="header">
          <div />
          <div />
        </header>
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
