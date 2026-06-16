import type { ReactNode } from "react";
import { Link } from "react-router-dom";
import AbilityIcon from "./AbilityIcon";
import type { Protection } from "../data/types";
import { PROTECTION_LABEL, PROT_RANK, PROT_SHORT, skill } from "../data";

export const PROT_COLOR: Record<Protection, string> = {
  iframe: "var(--iframe)", super_armor: "var(--sa)", frontal_guard: "var(--fg)", none: "var(--none)",
};

export function ProtMeter({ prot, title }: { prot: Protection; title?: string }) {
  const rank = PROT_RANK[prot];
  const color = PROT_COLOR[prot];
  return (
    <span className="prot" style={{ color }} title={title || PROTECTION_LABEL[prot]}>
      <span className="meter" aria-hidden="true">
        {[1, 2, 3, 4].map((n) => <i key={n} style={n <= rank ? { background: color } : undefined} />)}
      </span>
      {PROT_SHORT[prot]}
    </span>
  );
}

export function Kbd({ children }: { children: ReactNode }) {
  return <span className="kbd">{children}</span>;
}

export function CcBadges({ cc, none = "—" }: { cc: string[]; none?: string }) {
  if (!cc.length) return <span className="dim" style={{ fontSize: 11 }}>{none}</span>;
  return <>{cc.map((c) => <span key={c} className="badge cc" title="Crowd control">{c}</span>)}</>;
}

// Valkyrie route is flat — link to the Skills page anchor.
export function AbilityLink({ id }: { id: string }) {
  const s = skill(id);
  return (
    <Link className="ability-link" to={`/skills#${id}`}>
      <AbilityIcon id={id} />{s.name}
    </Link>
  );
}

export function KindBadge({ kind }: { kind: string }) {
  if (kind === "awakening") return null;
  const cls = kind === "pre-awakening" ? "preawk" : kind === "locked-only" ? "locked" : "optional";
  const label = kind === "pre-awakening" ? "PRE-AWK"
    : kind === "quick-slot" ? "QUICK-SLOT"
    : kind === "locked-only" ? "LOCKED"
    : kind.toUpperCase();
  return <span className={`badge ${cls}`}>{label}</span>;
}
