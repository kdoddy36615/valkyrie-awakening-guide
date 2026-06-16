import { useEffect, useMemo, useState } from "react";
import { useLocation } from "react-router-dom";
import { skills, protectionIn, PROTECTION_LABEL, KIND_LABEL } from "../data";
import type { Protection, Skill } from "../data/types";
import { PageHeader, Section, Callout } from "../components/Section";
import { ProtMeter, Kbd, KindBadge, PROT_COLOR } from "../components/badges";
import AbilityIcon from "../components/AbilityIcon";

const PROT_ORDER: Protection[] = ["iframe", "super_armor", "frontal_guard", "none"];
const KIND_ORDER = ["awakening", "pre-awakening", "rabam", "quick-slot", "locked-only"];

function SkillRow({ s, open, onToggle }: { s: Skill; open: boolean; onToggle: () => void }) {
  const prot = protectionIn(s, "pve");
  const imp = s.importance;
  return (
    <>
      <button className="lrow cols" id={s.id} onClick={onToggle}>
        <span><AbilityIcon id={s.id} size="row" /></span>
        <span className="nm">{s.name}</span>
        <span className="inp">{s.inputs.map((i, k) => <Kbd key={k}>{i}</Kbd>)}</span>
        <span className="bdgs">
          {prot && <ProtMeter prot={prot} title={s.protection?.tooltip_lines.join("; ")} />}
          <KindBadge kind={s.kind} />
        </span>
        <span className="dim" style={{ fontSize: "12px", overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap" }}>
          {s.usage_tags.join(" · ")}
        </span>
        <span className="barcell">
          {imp != null && (
            <span className="bar" title={`Importance ${imp}/10`}>
              <i style={{ width: `${imp * 10}%`, background: prot ? PROT_COLOR[prot] : "var(--accent)" }} />
            </span>
          )}
        </span>
        <span className="dpsv">{imp != null ? `${imp}/10` : "—"}</span>
        <span className="chev">{open ? "▾" : "▸"}</span>
      </button>
      {open && (
        <div className="lexp">
          <div className="facts">
            {s.cooldown && <div><span className="k">Cooldown</span>{s.cooldown}</div>}
            {s.mp_cost && <div><span className="k">MP</span>{s.mp_cost}</div>}
            {prot && <div><span className="k">Protection PvE</span>{PROTECTION_LABEL[prot]}</div>}
            {s.protection && <div><span className="k">Protection PvP</span>{PROTECTION_LABEL[s.protection.pvp]}</div>}
            {s.bdocodex_id && (
              <div><span className="k">Codex</span>
                <a href={s.protection?.source_url || `https://bdocodex.com/us/skill/${s.bdocodex_id}/`} target="_blank" rel="noreferrer">#{s.bdocodex_id}</a>
              </div>
            )}
            {!s.sheet_icon_matched && <div><span className="k">Sheet icon</span><span className="badge unknown">UNMATCHED</span></div>}
          </div>
          {s.description && <p className="note desc" style={{ marginTop: 10 }}>{s.description}</p>}
          {s.recommended_usage && (
            <p className="note" style={{ marginTop: 8 }}><b>Usage:</b> {s.recommended_usage}</p>
          )}
          {s.cc_lines.length > 0 && (
            <p className="note" style={{ marginTop: 8 }}><b>CC:</b> {s.cc_lines.join(" · ")}</p>
          )}
          {s.protection?.notes && (
            <p className="prov" style={{ marginTop: 8 }}>Protection note: {s.protection.notes}</p>
          )}
        </div>
      )}
    </>
  );
}

export default function SkillsPage() {
  const [q, setQ] = useState("");
  const [byProt, setByProt] = useState(false);
  const [openId, setOpenId] = useState<string | null>(null);
  const loc = useLocation();

  useEffect(() => {
    const hash = loc.hash.replace("#", "");
    if (hash) {
      setOpenId(hash);
      const el = document.getElementById(hash);
      if (el) el.scrollIntoView({ block: "center" });
    }
  }, [loc.hash]);

  const filtered = useMemo(() => {
    const needle = q.trim().toLowerCase();
    if (!needle) return skills;
    return skills.filter((s) =>
      s.name.toLowerCase().includes(needle) ||
      s.id.includes(needle) ||
      s.shortcodes.some((c) => c.toLowerCase().includes(needle)) ||
      s.usage_tags.some((t) => t.toLowerCase().includes(needle)),
    );
  }, [q]);

  const groups = useMemo(() => {
    if (byProt) {
      return PROT_ORDER.map((p) => ({
        key: p,
        title: PROTECTION_LABEL[p],
        items: filtered
          .filter((s) => protectionIn(s, "pve") === p)
          .sort((a, b) => (b.importance ?? -1) - (a.importance ?? -1)),
      })).filter((g) => g.items.length);
    }
    return KIND_ORDER.map((k) => ({
      key: k,
      title: KIND_LABEL[k],
      items: filtered.filter((s) => s.kind === k)
        .sort((a, b) => (b.importance ?? -1) - (a.importance ?? -1)),
    })).filter((g) => g.items.length);
  }, [filtered, byProt]);

  return (
    <>
      <PageHeader title="Skills">
        The canonical Skill Registry — identity, icons and protection from BDO Codex; importance and
        usage from the Discord guides. Sorted by importance within each group.
      </PageHeader>

      <div style={{ display: "flex", gap: 14, alignItems: "center", margin: "14px 0 4px", flexWrap: "wrap" }}>
        <input
          className="kbd" style={{ padding: "5px 10px", minWidth: 240, fontFamily: "inherit" }}
          placeholder="Search skills, shortcodes, tags…"
          value={q} onChange={(e) => setQ(e.target.value)}
        />
        <label style={{ display: "flex", gap: 6, alignItems: "center", fontSize: 12.5, color: "var(--text-dim)" }}>
          <input type="checkbox" checked={byProt} onChange={(e) => setByProt(e.target.checked)} />
          Group by protection tier (PvE)
        </label>
        <span className="dim" style={{ fontSize: 12 }}>{filtered.length} skills</span>
      </div>

      <Callout tag="GRADED">
        Protection is graded per mode: i-frame &gt; Super Armor &gt; Frontal Guard &gt; Unprotected. Rows show PvE; expand for PvP.
      </Callout>

      {groups.map((g) => (
        <Section key={g.key} id={`grp-${g.key}`} title={g.title} count={g.items.length}>
          <div className="thead cols">
            <span /><span>Skill</span><span>Input</span><span>Protection</span>
            <span>Usage</span><span>Importance</span><span className="r">Imp.</span><span />
          </div>
          {g.items.map((s) => (
            <SkillRow key={s.id} s={s} open={openId === s.id} onToggle={() => setOpenId(openId === s.id ? null : s.id)} />
          ))}
        </Section>
      ))}
    </>
  );
}
