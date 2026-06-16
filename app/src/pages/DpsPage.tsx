import { useMemo, useState } from "react";
import { dpsFile, skills, protectionIn } from "../data";
import { PageHeader, Callout } from "../components/Section";
import DpsTable from "../components/DpsTable";
import AbilityIcon from "../components/AbilityIcon";
import { ProtMeter, CcBadges } from "../components/badges";

function firstPct(lines: string[]): number {
  for (const l of lines) {
    const m = l.match(/([\d.]+)\s*%/);
    if (m) return parseFloat(m[1]);
  }
  return -1;
}

function PvpReference() {
  const [dir, setDir] = useState<1 | -1>(-1);
  const rows = useMemo(() => {
    const dmg = skills.filter((s) => s.pvp_damage.length > 0);
    return dmg
      .map((s) => ({ s, mod: firstPct(s.pvp_damage) }))
      .sort((a, b) => (a.mod - b.mod) * dir);
  }, [dir]);

  return (
    <table className="dps-table">
      <thead>
        <tr>
          <th>Skill</th>
          <th>Protection (PvP)</th>
          <th>CC (PvP)</th>
          <th className="num" style={{ cursor: "pointer" }} onClick={() => setDir((d) => (d === 1 ? -1 : 1))}>
            PvP dmg modifier{dir === 1 ? " ▲" : " ▼"}
          </th>
        </tr>
      </thead>
      <tbody>
        {rows.map(({ s }) => {
          const prot = protectionIn(s, "pvp");
          return (
            <tr key={s.id}>
              <td><AbilityIcon id={s.id} />{s.name}</td>
              <td>{prot && <ProtMeter prot={prot} title={s.protection?.tooltip_lines.join("; ")} />}</td>
              <td><CcBadges cc={s.cc_pvp} none="none in PvP" /></td>
              <td className="num" style={{ whiteSpace: "normal" }}>
                {s.pvp_damage.map((l, i) => <div key={i}>{l.replace(/ in PvP only$/, "")}</div>)}
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}

export default function DpsPage({ mode }: { mode: "pve" | "pvp" }) {
  const { meta, rows } = dpsFile;

  if (mode === "pvp") {
    return (
      <>
        <PageHeader title="DPS — PvP">
          The guide has no measured PvP DPS chart — only the PvE one. This is a PvP reference from
          BDO Codex: each damage skill's PvP damage modifier (the % of its damage that applies in
          PvP), its PvP protection, and the CC that still lands in PvP.
        </PageHeader>

        <Callout tag="NOT A DPS CHART" warn>
          These are Codex PvP damage multipliers + protection + CC, not measured PvP DPS. PvP DPS is
          not recomputed from the PvE chart (that would be misleading). Note many PvE CCs (Stiffness,
          Floating, Knockdown on a skill's PvE-only lines) do not apply in PvP.
        </Callout>

        <PvpReference />

        <p className="prov" style={{ marginTop: 12 }}>
          Source: BDO Codex tooltips (pulled {skillsPullDate()}). Protection differs from PvE only for
          movement skills (Death Line Chase / Shield Chase lose their PvE i-frame in PvP).
        </p>
      </>
    );
  }

  return (
    <>
      <PageHeader title="DPS — PvE">
        {meta.title} — {meta.author}. {meta.assumption}. Sortable; values are copied verbatim and
        never recomputed. Protection (PvE) and CC (PvE) shown per skill.
      </PageHeader>

      <Callout tag="LOCKED" warn>
        {meta.notes.join(" · ")}. {meta.locked_note}
      </Callout>

      <DpsTable rows={rows} />

      <p className="prov" style={{ marginTop: 12 }}>
        Source: {meta.source}. Cancel/combination rows (e.g. "Verdict Vult cancel",
        "Celestial Smite + abs. spear") are measurements mapped to their base skill, keeping the
        sheet label. See <a href="#/dps-pvp">DPS — PvP</a> for PvP modifiers.
      </p>
    </>
  );
}

function skillsPullDate(): string {
  const s = skills.find((x) => x.protection);
  return s?.protection?.pulled ?? "2026-06-15";
}
