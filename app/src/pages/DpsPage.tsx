import { useMemo, useState } from "react";
import { dpsFile, skillsFile, maybeSkill, protectionIn } from "../data";
import type { DpsRow, Skill } from "../data/types";
import { PageHeader, Callout } from "../components/Section";
import DpsTable from "../components/DpsTable";
import AbilityIcon from "../components/AbilityIcon";
import { ProtMeter, CcBadges } from "../components/badges";

const fmt = (v: number | null) =>
  v == null ? "—" : v.toLocaleString("en-US", { maximumFractionDigits: 1 });

// A single, unambiguous PvP damage factor for a skill, else null.
// null when the skill has 0 modifiers (a buff) or >1 (e.g. Verdict's two hit groups).
function pvpFactor(s: Skill | undefined): number | null {
  if (!s || s.pvp_damage.length !== 1) return null;
  const m = s.pvp_damage[0].match(/([\d.]+)\s*%/);
  return m ? parseFloat(m[1]) / 100 : null;
}

interface PvpRow { row: DpsRow; s: Skill | undefined; factor: number | null; est: number | null; reason: string | null; }

function buildPvpRows(rows: DpsRow[]): PvpRow[] {
  return rows.map((row) => {
    const s = maybeSkill(row.skill);
    const factor = pvpFactor(s);
    let est: number | null = null;
    let reason: string | null = null;
    if (!s) reason = "no matched skill";
    else if (row.also.length > 0) reason = "combination row (two skills, different modifiers)";
    else if (s.pvp_damage.length > 1) reason = "skill has multiple PvP modifiers";
    else if (s.pvp_damage.length === 0) reason = "no PvP damage modifier (buff/utility)";
    else if (row.dps == null) reason = "no base DPS";
    else if (factor != null) est = row.dps * factor;
    return { row, s, factor, est, reason };
  });
}

function PvpDpsTable() {
  const [sort, setSort] = useState<"est" | "pve">("est");
  const [dir, setDir] = useState<1 | -1>(-1);
  const rows = useMemo(() => {
    const out = buildPvpRows(dpsFile.rows);
    const key = (r: PvpRow) => (sort === "est" ? r.est : r.row.dps);
    out.sort((a, b) => {
      const av = key(a), bv = key(b);
      if (av == null && bv == null) return 0;
      if (av == null) return 1;   // nulls always last
      if (bv == null) return -1;
      return (av < bv ? -1 : av > bv ? 1 : 0) * dir;
    });
    return out;
  }, [sort, dir]);

  const click = (c: "est" | "pve") => {
    if (c === sort) setDir((d) => (d === 1 ? -1 : 1));
    else { setSort(c); setDir(-1); }
  };
  const arrow = (c: "est" | "pve") => (c === sort ? (dir === 1 ? " ▲" : " ▼") : "");

  return (
    <table className="dps-table">
      <thead>
        <tr>
          <th>Skill</th>
          <th>Prot (PvP)</th>
          <th>CC (PvP)</th>
          <th className="num" onClick={() => click("pve")}>PvE DPS{arrow("pve")}</th>
          <th className="num">× PvP mod</th>
          <th className="num" onClick={() => click("est")}>≈ PvP DPS{arrow("est")}</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(({ row, s, factor, est, reason }, i) => {
          const prot = s ? protectionIn(s, "pvp") : null;
          return (
            <tr key={i}>
              <td>{s && <AbilityIcon id={s.id} />}{row.name}</td>
              <td>{prot && <ProtMeter prot={prot} title={s?.protection?.tooltip_lines.join("; ")} />}</td>
              <td>{s ? <CcBadges cc={s.cc_pvp} none="none" /> : "—"}</td>
              <td className="num">{fmt(row.dps)}</td>
              <td className="num">{factor != null ? `${(factor * 100).toLocaleString("en-US", { maximumFractionDigits: 2 })}%` : "—"}</td>
              <td className="num" title={reason ? `Not computed: ${reason}` : undefined}>
                {est != null ? fmt(Math.round(est)) : <span className="dim">—</span>}
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
          The guide has no measured PvP DPS chart. This estimates one by scaling each locked PvE DPS
          value by the skill's Codex PvP damage modifier (≈ PvP DPS = PvE DPS × modifier), alongside
          PvP protection and the CC that still lands in PvP.
        </PageHeader>

        <Callout tag="ESTIMATE" warn>
          ≈ PvP DPS is a naive scalar estimate, not a measurement. It assumes the same gear/context as
          the PvE chart and applies only the flat PvP damage multiplier — it does <b>not</b> account
          for PvP losing PvE-only mechanics (e.g. guaranteed Crit +100% PvE-only), or for AP/DP and
          crit differences vs a player target, so real PvP burst is typically lower. Rows that combine
          two skills (cancels like "Counter + S.Throw") or skills with two modifiers (Verdict) are
          left blank — there's no single factor to apply.
        </Callout>

        <PvpDpsTable />

        <p className="prov" style={{ marginTop: 12 }}>
          PvE DPS from the locked chart (verbatim). PvP modifier + protection + CC from BDO Codex
          (pulled {skillsPullDate()}). Protection differs from PvE only for movement skills
          (Death Line Chase / Shield Chase lose their PvE i-frame in PvP).
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
  return skillsFile.meta.pull_date;
}
