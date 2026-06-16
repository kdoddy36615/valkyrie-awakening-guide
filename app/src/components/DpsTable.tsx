import { useMemo, useState } from "react";
import type { DpsRow } from "../data/types";
import { maybeSkill, protectionIn } from "../data";
import AbilityIcon from "./AbilityIcon";
import { ProtMeter, CcBadges } from "./badges";

const fmt = (v: number | null) =>
  v == null ? "—" : v.toLocaleString("en-US", { maximumFractionDigits: 1 });

type Col = "name" | "hits" | "damage" | "total" | "duration" | "dps";
const NUM_COLS: Col[] = ["hits", "damage", "total", "duration", "dps"];

export default function DpsTable({ rows }: { rows: DpsRow[] }) {
  const [sort, setSort] = useState<Col>("dps");
  const [dir, setDir] = useState<1 | -1>(-1);

  const sorted = useMemo(() => {
    const out = [...rows];
    out.sort((a, b) => {
      if (sort === "name") return a.name.localeCompare(b.name) * dir;
      const av = a[sort] ?? -Infinity;
      const bv = b[sort] ?? -Infinity;
      return (av < bv ? -1 : av > bv ? 1 : 0) * dir;
    });
    return out;
  }, [rows, sort, dir]);

  const click = (c: Col) => {
    if (c === sort) setDir((d) => (d === 1 ? -1 : 1));
    else { setSort(c); setDir(c === "name" ? 1 : -1); }
  };
  const arrow = (c: Col) => (c === sort ? (dir === 1 ? " ▲" : " ▼") : "");

  return (
    <table className="dps-table">
      <thead>
        <tr>
          <th onClick={() => click("name")}>Skill{arrow("name")}</th>
          <th>Prot (PvE)</th>
          <th>CC (PvE)</th>
          {NUM_COLS.map((c) => (
            <th key={c} className="num" onClick={() => click(c)}>
              {c === "duration" ? "Dur (s)" : c[0].toUpperCase() + c.slice(1)}{arrow(c)}
            </th>
          ))}
        </tr>
      </thead>
      <tbody>
        {sorted.map((r, i) => {
          const s = maybeSkill(r.skill);
          const prot = s ? protectionIn(s, "pve") : null;
          return (
            <tr key={i}>
              <td>
                {s && <AbilityIcon id={s.id} />}
                {r.name}
                {!r.skill && <span className="badge unknown" title="No matched skill">?</span>}
              </td>
              <td>{prot ? <ProtMeter prot={prot} title={`PvE protection: ${s!.protection!.tooltip_lines.join("; ") || s!.name}`} /> : <span className="dim">—</span>}</td>
              <td>{s ? <CcBadges cc={s.cc} /> : <span className="dim">—</span>}</td>
              <td className="num">{fmt(r.hits)}</td>
              <td className="num">{fmt(r.damage)}</td>
              <td className="num">{fmt(r.total)}</td>
              <td className="num">{fmt(r.duration)}</td>
              <td className="num">{fmt(r.dps)}</td>
            </tr>
          );
        })}
      </tbody>
    </table>
  );
}
