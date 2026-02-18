import { Link, NavLink, Outlet } from "react-router-dom";
import Breadcrumb from "./Breadcrumb";

function navClass({ isActive }: { isActive: boolean }) {
  return isActive ? "active" : "";
}

export default function Layout() {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <Link to="/" className="sidebar-brand">
          <img src="/favicon.svg" alt="" width="20" height="20" />
          Pipeline Review
        </Link>
        <nav>
          <ul className="sidebar-nav">
            <li>
              <NavLink to="/" end className={navClass}>
                Shows
              </NavLink>
            </li>
            <li>
              <NavLink to="/search" className={navClass}>
                Search
              </NavLink>
            </li>
          </ul>
        </nav>
      </aside>
      <div className="main-area">
        <header className="header">
          <Breadcrumb />
        </header>
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
