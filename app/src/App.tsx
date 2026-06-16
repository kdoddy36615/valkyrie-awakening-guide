import { useState } from "react";
import { NavLink, Navigate, Route, Routes } from "react-router-dom";
import { NAV, NAV_GROUPS } from "./toc";
import ronnieImg from "./assets/authors/ronnie.png";
import sarronImg from "./assets/authors/sarron.png";
import vesImg from "./assets/authors/ves.png";
import SkillsPage from "./pages/SkillsPage";
import CombosPage from "./pages/CombosPage";
import PracticePage from "./pages/PracticePage";
import SetupPage from "./pages/SetupPage";
import TricksPage from "./pages/TricksPage";
import DpsPage from "./pages/DpsPage";
import VideosPage from "./pages/VideosPage";
import ReferencePage from "./pages/ReferencePage";
import R1Page from "./pages/R1Page";
import FeedbackModal from "./components/FeedbackModal";

const SHEET_URL = "https://docs.google.com/spreadsheets/d/1yA9tOQ1izphHaUoa0Zi51I47E78_x0CmvipZSBmt9aM/edit?gid=0#gid=0";

function Sidebar({ onFeedback }: { onFeedback: () => void }) {
  const [open, setOpen] = useState(false);
  return (
    <nav className={open ? "side open" : "side"}>
      <div className="brand">
        <div className="t">Awakening <em>Valkyrie</em></div>
        <div className="s">GUIDE 2026 · STUDY APP</div>
        <button className="hamburger" onClick={() => setOpen((o) => !o)} aria-label="Toggle menu">≡</button>
        <div className="brand-src">
          <div className="h">Sources</div>
          <div className="r"><span className="m">SHEET</span> <a href={SHEET_URL} target="_blank" rel="noreferrer" title="Valkyrie Guide 2026 — maintained by Ves [SRPH]"><img className="nameplate" style={{ height: 24 }} src={vesImg} alt="Ves [SRPH]" /></a></div>
          <div className="r"><span className="m">PVE</span> <img className="nameplate" style={{ height: 22 }} src={ronnieImg} alt="RoNNiE# [SRPH]" title="RoNNiE# [SRPH] — Awakening PvE specialist" /></div>
          <div className="r"><span className="m">PVP</span> <img className="nameplate" style={{ height: 28 }} src={sarronImg} alt="Sarron [FAT]" title="Sarron [FAT] — Moderator, PvP" /></div>
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
        <button className="r feedback" onClick={onFeedback}>
          <span className="m">✉</span>Feedback
        </button>
      </div>
    </nav>
  );
}

export default function App() {
  const [feedbackOpen, setFeedbackOpen] = useState(false);
  return (
    <div className="app">
      <Sidebar onFeedback={() => setFeedbackOpen(true)} />
      {feedbackOpen && <FeedbackModal onClose={() => setFeedbackOpen(false)} />}
      <main className="main">
        <Routes>
          <Route path="/" element={<Navigate to="/skills" replace />} />
          <Route path="/skills" element={<SkillsPage />} />
          <Route path="/combos" element={<CombosPage />} />
          <Route path="/practice" element={<PracticePage />} />
          <Route path="/setup-pve" element={<SetupPage mode="pve" />} />
          <Route path="/setup-pvp" element={<SetupPage mode="pvp" />} />
          <Route path="/tricks" element={<TricksPage />} />
          <Route path="/dps" element={<DpsPage mode="pve" />} />
          <Route path="/dps-pvp" element={<DpsPage mode="pvp" />} />
          <Route path="/videos" element={<VideosPage />} />
          <Route path="/reference" element={<ReferencePage />} />
          <Route path="/r1" element={<R1Page />} />
          <Route path="*" element={<Navigate to="/skills" replace />} />
        </Routes>
      </main>
    </div>
  );
}
