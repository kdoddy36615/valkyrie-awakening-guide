import { useState } from "react";
import { combos } from "../data";
import type { Mode } from "../data/types";
import { PageHeader } from "../components/Section";
import ComboStrip from "../components/ComboStrip";

type Filter = "all" | "pve" | "pvp";

export default function PracticePage() {
  const [filter, setFilter] = useState<Filter>("all");
  const list = combos.filter((c) => filter === "all" || c.mode === filter);

  return (
    <>
      <PageHeader title="Practice">
        The combo strips, chrome stripped — for a second monitor while you drill. No quiz, no meta;
        just inputs, icons and protection.
      </PageHeader>

      <div style={{ display: "flex", gap: 8, margin: "12px 0 4px" }}>
        {(["all", "pve", "pvp"] as Filter[]).map((f) => (
          <button
            key={f}
            className={filter === f ? "kbd" : "kbd"}
            style={{
              cursor: "pointer", padding: "4px 12px",
              borderColor: filter === f ? "var(--accent)" : "var(--border-strong)",
              color: filter === f ? "var(--accent)" : "var(--text-dim)",
            }}
            onClick={() => setFilter(f)}
          >
            {f.toUpperCase()}
          </button>
        ))}
      </div>

      {list.map((c) => (
        <div key={c.id} style={{ marginTop: 18 }}>
          <div className="micro" style={{ marginBottom: 0 }}>
            {c.name}{c.core_variant ? ` — ${c.core_variant}` : ""}
          </div>
          <ComboStrip combo={{ steps: c.steps, notes: [] }} mode={c.mode as Mode} />
        </div>
      ))}
    </>
  );
}
