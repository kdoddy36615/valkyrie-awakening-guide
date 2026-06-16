import skillsJson from "../../../data/skills.json";
import combosJson from "../../../data/combos.json";
import dpsJson from "../../../data/dps.json";
import tricksJson from "../../../data/tricks.json";
import theoryJson from "../../../data/theory.json";
import type {
  SkillsFile, Skill, CombosFile, Combo, DpsFile, TricksFile, TheoryFile,
  Mode, Protection,
} from "./types";

export const skillsFile = skillsJson as unknown as SkillsFile;
export const skills: Skill[] = skillsFile.skills;
export const combosFile = combosJson as unknown as CombosFile;
export const combos: Combo[] = combosFile.combos;
export const dpsFile = dpsJson as unknown as DpsFile;
export const tricksFile = tricksJson as unknown as TricksFile;
export const theoryFile = theoryJson as unknown as TheoryFile;

export const skillById = new Map(skills.map((s) => [s.id, s]));
export function skill(id: string): Skill {
  const s = skillById.get(id);
  if (!s) throw new Error(`Unknown skill id: ${id}`);
  return s;
}
export function maybeSkill(id: string | null | undefined): Skill | undefined {
  return id ? skillById.get(id) : undefined;
}

// Alias table — fold every shortcode + roster typo so Discord shortcodes resolve.
export const ALIAS = new Map<string, string>();
for (const s of skills) {
  for (const code of s.shortcodes) {
    ALIAS.set(code.toLowerCase(), s.id);
    ALIAS.set(code.replace(/[^a-z0-9]/gi, "").toLowerCase(), s.id); // bare form
  }
}
export function resolveAlias(code: string): string | undefined {
  return ALIAS.get(code.toLowerCase()) ?? ALIAS.get(code.replace(/[^a-z0-9]/gi, "").toLowerCase());
}

export const PROTECTION_LABEL: Record<Protection, string> = {
  iframe: "i-frame", super_armor: "Super Armor", frontal_guard: "FG", none: "Unprotected",
};
export const PROT_RANK: Record<Protection, number> = {
  iframe: 4, super_armor: 3, frontal_guard: 2, none: 1,
};
export const PROT_SHORT: Record<Protection, string> = {
  iframe: "IFRAME", super_armor: "SA", frontal_guard: "FG", none: "UNPROT",
};

export function protectionIn(s: Skill, mode: Mode): Protection | null {
  return s.protection ? s.protection[mode] : null;
}

export const KIND_LABEL: Record<string, string> = {
  awakening: "Awakening",
  "pre-awakening": "Pre-awakening",
  rabam: "Rabam",
  "quick-slot": "Quick-slot",
  "locked-only": "Locked",
};

// DEV-only referential check (canonical validator is scripts/validate_data.py).
if (import.meta.env.DEV) {
  const missing: string[] = [];
  const chk = (id: string | null | undefined, where: string) => {
    if (id && !skillById.has(id)) missing.push(`${where}: ${id}`);
  };
  for (const c of combos)
    c.steps.forEach((st, i) => {
      chk(st.skill, `${c.id}[${i}]`);
      st.choices?.forEach((x) => chk(x, `${c.id}[${i}]`));
    });
  for (const r of dpsFile.rows) chk(r.skill, `dps:${r.name}`);
  if (missing.length) console.error("Data reference errors:", missing);
}
