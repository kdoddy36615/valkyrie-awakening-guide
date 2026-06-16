import { useState } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import { NAV, NAV_GROUPS } from "./toc";
import SkillsPage from "./pages/SkillsPage";
import CombosPage from "./pages/CombosPage";
import PracticePage from "./pages/PracticePage";
import AddonsPage from "./pages/AddonsPage";
import TricksPage from "./pages/TricksPage";
import DpsPage from "./pages/DpsPage";
import ReferencePage from "./pages/ReferencePage";
import R1Page from "./pages/R1Page";

function Sidebar() {
  const [open, setOpen] = useState(false);
  return (
    <nav className={open ? "side open" : "side"}>
      <div className="brand">
        <div className="t">Awakening <em>Valkyrie</em></div>
        <div className="s">GUIDE 2026 · STUDY APP</div>
        <button className="hamburger" onClick={() => setOpen((o) => !o)} aria-label="Toggle menu">≡</button>
        <div className="brand-src">
          <div className="h">Sources</div>
          <div className="r"><span className="m">SHEET</span> Valkyrie Guide 2026</div>
          <div className="r"><span className="m">PVE</span> RoNNiE (Discord)</div>
          <div className="r"><span className="m">PVP</span> Sarron (Discord)</div>
        </div>
      </div>
      <div className="nav-area">
        {NAV_GROUPS.map((g) => (
          <div key={g}>
            <span className="grp">{g}</span>
            {NAV.filter((n) => n.group === g).map((n) => (
              <NavLink
                key={n.path}
                to={n.path}
                className={({ isActive }) => (isActive ? "nav active" : "nav")}
                onClick={() => setOpen(false)}
              >
                <span>{n.label}</span>
              </NavLink>
            ))}
          </div>
        ))}
      </div>
      <div className="credits">
        <div className="r"><span className="m">PROT</span> BDO Codex</div>
      </div>
    </nav>
  );
}

export default function App() {
  return (
    <div className="app">
      <Sidebar />
      <main className="main">
        <Routes>
          <Route path="/" element={<Navigate to="/skills" replace />} />
          <Route path="/skills" element={<SkillsPage />} />
          <Route path="/combos" element={<CombosPage />} />
          <Route path="/practice" element={<PracticePage />} />
          <Route path="/addons" element={<AddonsPage />} />
          <Route path="/tricks" element={<TricksPage />} />
          <Route path="/dps" element={<DpsPage mode="pve" />} />
          <Route path="/dps-pvp" element={<DpsPage mode="pvp" />} />
          <Route path="/reference" element={<ReferencePage />} />
          <Route path="/r1" element={<R1Page />} />
          <Route path="*" element={<Navigate to="/skills" replace />} />
        </Routes>
      </main>
    </div>
  );
}
