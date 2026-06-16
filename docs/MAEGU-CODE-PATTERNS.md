# Maegu code patterns — inlined so you never open `C:\Users\kevin\projects\maegu`

A prior instance read the whole maegu reference tree; the reusable source is reproduced here
(verbatim where it drops in as-is, with **VALKYRIE ADAPT** notes where the simpler IA changes it).
Combined with `docs/IMPLEMENTATION-NOTES.md`, this is everything you need — **do not open the maegu
repo**. The static scaffold (package.json, vite/tsconfig, index.html, main.tsx, vite-env, styles.css)
is already written and retinted; this doc is for the `app/src` components, the data layer, and scripts.

Routing reminder: **Valkyrie has no global PVE|PVP mode toggle.** Pages are flat: Skills, Combos,
Practice, Add-ons, Tricks, DPS, Reference, R1 AOS. Use `HashRouter` + a Sidebar `NavLink` list +
one route per page (`/:page`). The Combos page *internally* sections PvE / PvP-AOS-1v1 / PvP-Large-Scale.
Per-skill protection is still per-mode (`pve`/`pvp`) in the data; just pick which to show in context.

---

## app/src/components/AbilityIcon.tsx — drops in VERBATIM

```tsx
// Skill icons fetched from BDO Codex (scripts/fetch_icons.py), named by canonical skill id.
const icons = import.meta.glob("../assets/icons/*.webp", {
  eager: true, query: "?url", import: "default",
}) as Record<string, string>;

export function iconUrl(skillId: string): string | undefined {
  return icons[`../assets/icons/${skillId}.webp`];
}

export default function AbilityIcon({ id, size = "sm" }: { id: string; size?: "sm" | "row" | "xl" }) {
  const url = iconUrl(id);
  if (!url) return null;            // unmatched icons are flagged in data, never block render
  return <img className={`ability-icon ${size}`} src={url} alt="" loading="lazy" />;
}
```

## app/src/components/SourceImage.tsx — VERBATIM (framed thumb + Esc-closes lightbox)

```tsx
import { useEffect, useState } from "react";
// Resolve "sources/..." OR "assets/addons/..." paths. Pick the glob that matches where you put
// the add-on screenshots; maegu globbed sources/. Add-on shots can live in app/src/assets/addons.
const images = import.meta.glob("../../../sources/**/*.png", { eager: true, query: "?url", import: "default" }) as Record<string, string>;
function resolve(p: string) { return images[`../../../${p}`]; }

export default function SourceImage({ path, alt }: { path: string; alt: string }) {
  const url = resolve(path);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);
  if (!url) return <p className="note">Missing image: {path}</p>;
  return (<>
    <figure className="thumb">
      <button type="button" onClick={() => setOpen(true)} title="Click to zoom"><img src={url} alt={alt} loading="lazy" /></button>
      <figcaption>{alt} — click to zoom</figcaption>
    </figure>
    {open && <div className="lightbox" onClick={() => setOpen(false)} role="dialog" aria-label={alt}><img src={url} alt={alt} /></div>}
  </>);
}
```

## app/src/components/Section.tsx — VERBATIM minus the mode badge

```tsx
import type { ReactNode } from "react";

export function Section({ id, title, count, desc, children }:
  { id: string; title: string; count?: number | string; desc?: string; children: ReactNode }) {
  return (
    <section className="sec" id={id}>
      <div className="sechead">
        <h2>{title}</h2>
        {count != null && <span className="cnt">{count}</span>}
        {desc && <span className="d">{desc}</span>}
      </div>
      {children}
    </section>
  );
}
// VALKYRIE ADAPT: PageHeader has no mode badge (no global mode). Just an h1 + dim subtitle.
export function PageHeader({ title, children }: { title: string; children?: ReactNode }) {
  return (<><h1 className="h1">{title}</h1><p className="page-sub">{children}</p></>);
}
export function Callout({ tag, warn, children }: { tag?: string; warn?: boolean; children: ReactNode }) {
  return (<div className={warn ? "callout warn" : "callout"}>{tag && <span className="tag">{tag}</span>}<span>{children}</span></div>);
}
```

## app/src/components/badges.tsx — ProtMeter VERBATIM; AbilityLink re-routed

The graded 4-dot meter + mono label, FG as its own middle tier. `PROT_COLOR`, `ProtMeter`, `CcBadges`
drop in as-is. `AbilityLink` must change to the flat route.

```tsx
import { Link } from "react-router-dom";
import AbilityIcon from "./AbilityIcon";
import type { Protection } from "../data/types";
import { PROTECTION_LABEL, PROT_RANK, PROT_SHORT, skill } from "../data";

export const PROT_COLOR: Record<Protection, string> = {
  iframe: "var(--iframe)", super_armor: "var(--sa)", frontal_guard: "var(--fg)", none: "var(--none)",
};
export function ProtMeter({ prot, title }: { prot: Protection; title?: string }) {
  const rank = PROT_RANK[prot]; const color = PROT_COLOR[prot];
  return (
    <span className="prot" style={{ color }} title={title || PROTECTION_LABEL[prot]}>
      <span className="meter" aria-hidden="true">
        {[1,2,3,4].map((n) => <i key={n} style={n <= rank ? { background: color } : undefined} />)}
      </span>{PROT_SHORT[prot]}
    </span>
  );
}
export function Kbd({ children }: { children: React.ReactNode }) { return <span className="kbd">{children}</span>; }
// VALKYRIE ADAPT: route is flat — link to the Skills page anchor.
export function AbilityLink({ id }: { id: string }) {
  const s = skill(id);
  return <Link className="ability-link" to={`/skills#${id}`}><AbilityIcon id={id} />{s.name}</Link>;
}
```

## app/src/components/ComboStrip.tsx — the centerpiece, VALKYRIE ADAPT

Maegu's strip shows input-above-icon, OR-stacks for `choices`, OPTIONAL captions. **Valkyrie adds a
category label caption per step** (`FLOATING`/`TRANSITION`/`CRIT BUFF`/…, the `.strip-cat` class) and a
per-mode protection badge. Shape:

```tsx
import { Fragment } from "react";
import type { Combo, ComboStep, Mode } from "../data/types";
import { skill, protectionIn } from "../data";
import { ProtMeter } from "./badges";
import AbilityIcon from "./AbilityIcon";

function Choice({ id, input, mode }: { id: string; input?: string; mode: Mode }) {
  const s = skill(id);
  const prot = protectionIn(s, mode);
  return (
    <span className="strip-choice">
      {input && <span className="strip-input">{input}</span>}
      <span title={s.name}><AbilityIcon id={id} size="xl" /></span>
      {prot && <ProtMeter prot={prot} title={s.protection.tooltip_lines.join("; ")} />}
    </span>
  );
}
function Step({ step, mode }: { step: ComboStep; mode: Mode }) {
  return (
    <div className="strip-step" title={step.annotation}>
      {step.category && <span className="strip-cat">{step.category.replace(/-/g, " ")}</span>}
      {step.choices && step.choices.length > 1 ? (
        step.choices.map((id, j) => (
          <Fragment key={id}>{j > 0 && <span className="strip-or">OR</span>}
            <Choice id={id} input={j === 0 ? step.input : undefined} mode={mode} /></Fragment>
        ))
      ) : (
        <Choice id={step.skill!} input={step.input} mode={mode} />
      )}
      {step.optional && <span className="strip-optional">OPTIONAL</span>}
    </div>
  );
}
export default function ComboStrip({ combo, mode }: { combo: Pick<Combo,"steps"|"notes">; mode: Mode }) {
  return (
    <div>
      <div className="combo-strip">{combo.steps.map((s, i) => <Step key={i} step={s} mode={mode} />)}</div>
      {combo.notes?.length ? <ul className="notes strip-notes">{combo.notes.map((n,i)=><li key={i}>{n}</li>)}</ul> : null}
    </div>
  );
}
```
**Practice page** = the same `<ComboStrip>` rendered chrome-stripped (no card/meta), per HANDOFF §8.

## app/src/components/DpsTable.tsx — render the locked rows VERBATIM, never recompute

`fmt = v == null ? "—" : v.toLocaleString("en-US",{maximumFractionDigits:1})`. Valkyrie's dps.json
rows are `{ skill, name, hits, damage, total, duration, dps }` (see HANDOFF data model). Render one
row each, with the sheet label (`name`), a skill icon when `skill` resolves, and the numeric columns
right-aligned (`td.num`). Make the `th` sortable (the `.dps-table th` cursor is already styled).
Keep the header provenance line (@RonnieBDO, "60%", "not frame exact") above the table.

---

## app/src/data/index.ts — the data-layer pattern (KEY)

Loads `data/*.json`, casts `as unknown as <File>`, builds the id index and the rules the ADRs lock.
The maegu shape, mapped to Valkyrie:

```ts
import skillsJson from "../../../data/skills.json";
import combosJson from "../../../data/combos.json";
import dpsJson from "../../../data/dps.json";
import tricksJson from "../../../data/tricks.json";
import theoryJson from "../../../data/theory.json";
import type { SkillsFile, Skill, Mode, Protection /*…*/ } from "./types";

export const skillsFile = skillsJson as unknown as SkillsFile;
export const skills: Skill[] = skillsFile.skills;
export const skillById = new Map(skills.map((s) => [s.id, s]));
export function skill(id: string): Skill { const s = skillById.get(id); if (!s) throw new Error(`Unknown skill id: ${id}`); return s; }

// Alias table — fold EVERY shortcode + roster typo so Discord combos resolve.
export const ALIAS = new Map<string, string>();
for (const s of skills) for (const code of s.shortcodes) ALIAS.set(code.toLowerCase(), s.id);
// also fold known typos: Inpulsa->divina-impulsa, Promptess->promptness, Hastludium->hastiludium,
// PrimeSanctitasDeEnslar->sanctitas-de-enslar (do this in build_skills.py so it ships in shortcodes[]).

export const PROTECTION_LABEL: Record<Protection,string> = { iframe:"i-frame", super_armor:"Super Armor", frontal_guard:"FG", none:"Unprotected" };
export const PROT_RANK: Record<Protection,number> = { iframe:4, super_armor:3, frontal_guard:2, none:1 };
export const PROT_SHORT: Record<Protection,string> = { iframe:"IFRAME", super_armor:"SA", frontal_guard:"FG", none:"UNPROT" };
export function protectionIn(s: Skill, mode: Mode): Protection | null { return s.protection[mode]; }

// DEV-only referential check (canonical validator is scripts/validate_data.py)
if (import.meta.env.DEV) {
  const missing: string[] = [];
  const chk = (id: string | null | undefined, where: string) => { if (id && !skillById.has(id)) missing.push(`${where}: ${id}`); };
  for (const c of combosJson.combos) c.steps.forEach((st: any, i: number) => { chk(st.skill, `${c.id}[${i}]`); st.choices?.forEach((x: string) => chk(x, `${c.id}[${i}]`)); });
  if (missing.length) console.error("Data reference errors:", missing);
}
```

---

## scripts/build_skills.py — shape (REGISTRY + tooltips merge)

Mirror maegu's `build_abilities.py`. The REGISTRY list is **already curated** in
`research/bdocodex/REGISTRY-DATA.md` (+ `roster_id_map.json` + `protection_curated.json`). For each
roster skill: pull its record from `research/bdocodex/tooltips.json` (description, input, cooldown,
mp, effects, cc lines via `Bound|Knockdown|Stun|Stiffness|Floating|Knockback`), attach the curated
graded `protection.{pve,pvp}` + `tooltip_lines` + `source="BDO Codex"` + `source_url` + `pulled`,
add Discord metadata (importance/usage_tags/recommended_usage from `sources/skill-roster.md` +
the discord md), `shortcodes` (incl. every typo), `kind`, `inputs`. Constants:
`PULL_DATE = "2026-06-15"`, `TOOLTIP_SOURCE = "BDO Codex"`. Name comes from Codex (e.g. **Divina
Inpulsa**), id stays the roster id (`divina-impulsa`).

## scripts/fetch_icons.py — copy the already-downloaded icons

Icons are already pulled to `research/bdocodex/icons/<bdocodex_id>.webp`. This script just copies each
to `app/src/assets/icons/<roster-id>.webp` using `research/bdocodex/roster_id_map.json` (reuse if the
dest exists; only hit the network for a skill missing locally, via the raw-HTML `<img … width="40">`
path like maegu).

## scripts/validate_data.py — VERBATIM logic, swap id_fields

Load `data/skills.json` → `IDS`. `walk()` combos/dps/tricks/theory recursively; any field in
`id_fields = {"skill","skills","choices","skill_refs", …}` must resolve to a known id (null allowed
for flagged-unmatched). `sys.exit(1)` with messages on error, else print OK. **Must exit 0** (Phase 4).

## scripts/smoke.mjs — VERBATIM puppeteer-core harness, swap routes

`executablePath` candidates already correct for this machine (Chrome at
`C:\Program Files\Google\Chrome\Application\chrome.exe`, Edge fallback). Replace the route list with
the flat hash routes: `/#/skills /#/combos /#/practice /#/addons /#/tricks /#/dps /#/reference /#/r1`.
Fail on console errors / pageerrors / HTTP≥400 / `<200` chars; screenshot each to `.screenshots/`.
```
const routes = [["skills","/#/skills"],["combos","/#/combos"],["practice","/#/practice"],
  ["addons","/#/addons"],["tricks","/#/tricks"],["dps","/#/dps"],["reference","/#/reference"],["r1","/#/r1"]];
```

The full `parse_tooltips.py` already exists at `research/bdocodex/parse_tooltips.py` (don't rewrite it).
