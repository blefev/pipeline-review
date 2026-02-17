import { NavLink, Outlet } from "react-router-dom";
import Breadcrumb from "./Breadcrumb";
import SeedButton from "./SeedButton";

export default function Layout() {
  return (
    <div className="app-layout">
      <aside className="sidebar">
        <div className="sidebar-brand">Pipeline Review</div>
        <nav>
          <ul className="sidebar-nav">
            <li>
              <NavLink to="/" end>
                Shows
              </NavLink>
            </li>
            <li>
              <NavLink to="/search">Search</NavLink>
            </li>
          </ul>
        </nav>
      </aside>
      <div className="main-area">
        <header className="header">
          <Breadcrumb />
          <SeedButton />
        </header>
        <main className="page-content">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
