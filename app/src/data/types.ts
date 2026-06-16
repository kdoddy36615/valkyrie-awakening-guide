// Shapes for data/*.json. The Registry (skills.json) is canonical; combos, dps,
// tricks and theory reference skills by id. See CONTEXT.md / docs/adr for the model.

export type Mode = "pve" | "pvp";
export type Scale = "1v1" | "large-scale";
export type Protection = "iframe" | "super_armor" | "frontal_guard" | "none";
export type SkillKind =
  | "awakening"
  | "pre-awakening"
  | "rabam"
  | "quick-slot"
  | "locked-only";

export interface SkillProtection {
  pve: Protection;
  pvp: Protection;
  tooltip_lines: string[];
  notes: string;
  source: string;
  source_url: string | null;
  pulled: string;
}

export interface Skill {
  id: string;
  name: string;
  kind: SkillKind;
  shortcodes: string[];
  inputs: string[];
  icon: string;
  importance: number | null;
  usage_tags: string[];
  recommended_usage: string;
  protection: SkillProtection | null;
  description: string | null;
  cooldown: string | null;
  mp_cost: string | null;
  required_level: number | null;
  effects: string[];
  cc_lines: string[];
  cc: string[];
  cc_pvp: string[];
  pvp_damage: string[];
  bdocodex_id: number | null;
  sheet_icon_matched: boolean;
}

export interface SkillsFile {
  meta: {
    pull_date: string;
    tooltip_source: string;
    core_skill: string;
    protection_enum: Protection[];
    count: number;
    note: string;
  };
  skills: Skill[];
}

export interface ComboStep {
  skill?: string | null;
  choices?: string[];
  input?: string;
  category: string | null;
  category_raw: string | null;
  optional: boolean;
  annotation: string | null;
  phase: string | null;
}

export interface ComboSource {
  source: "sheet" | "discord";
  ref: string;
  updated?: string;
}

export interface Combo {
  id: string;
  mode: Mode;
  scale: Scale | null;
  protected: boolean;
  family: string;
  core_variant: string | null;
  name: string;
  video: string | null;
  steps: ComboStep[];
  notes: string[];
  sources: ComboSource[];
  conflicts: string[];
}

export interface CombosFile {
  meta: { count: number; category_enum: string[]; note: string };
  combos: Combo[];
}

export interface DpsRow {
  skill: string | null;
  name: string;
  also: string[];
  hits: number | null;
  damage: number | null;
  total: number | null;
  duration: number | null;
  dps: number | null;
}

export interface DpsFile {
  meta: {
    title: string;
    source: string;
    author: string;
    assumption: string;
    notes: string[];
    locked: boolean;
    locked_note: string;
    columns: string[];
  };
  rows: DpsRow[];
}

export type TrickType = "cancel" | "tip" | "transition" | "movement" | "macro";

export interface TrickRow {
  input: string;
  protected: string;
}

export interface Trick {
  id: string;
  name: string;
  type: TrickType;
  icons: string[];
  sequences: string[];
  rows?: TrickRow[];
  notes: string[];
  comment: string | null;
  video: string | null;
}

export interface TricksFile {
  meta: { source: string; note: string; types: TrickType[] };
  tricks: Trick[];
}

export interface TheoryEntry {
  skill: string;
  input: string;
  note: string | null;
}

export interface TheoryGroup {
  label: string;
  entries: TheoryEntry[];
  pros?: string[];
  cons?: string[];
}

export interface TheorySection {
  id: string;
  title: string;
  desc: string;
  groups: TheoryGroup[];
  notes: string[];
}

export interface TheoryFile {
  meta: { source: string; updated: string; note: string };
  sections: TheorySection[];
}

export interface SetupEntry {
  skill: string | null;
  name?: string;
  note?: string;
  tier?: string;
}

export interface SetupModeAddon {
  image: string;
  author: string;
  caption: string;
  breakdown: string[];
}

export interface SetupMode {
  core: SetupEntry[];
  core_note: string;
  rabams: SetupEntry[];
  rabam_note: string;
  addon: SetupModeAddon;
  locked: SetupEntry[];
  locked_note: string;
  downsmash?: SetupEntry[];
  downsmash_note?: string;
  pvp_unlocks?: SetupEntry[];
}

export interface SetupFile {
  meta: { note: string; sources: Record<string, string> };
  quickslot: SetupEntry[];
  modes: { pve: SetupMode; pvp: SetupMode };
}

export interface Buff {
  skill?: string | null;
  skills?: string[];
  name?: string;
  text: string;
}

export interface BuffsFile {
  meta: { source: string; note: string };
  buffs: Buff[];
}

export interface VideoLink {
  label: string;
  url: string;
  author: string;
}

export interface VideoGroup {
  title: string;
  note: string;
  videos: VideoLink[];
}

export interface VideosFile {
  meta: { note: string; count: number };
  groups: VideoGroup[];
}
