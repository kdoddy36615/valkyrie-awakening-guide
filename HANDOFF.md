# Valkyrie Awakening App — Implementation Handoff

You are picking up a planned-but-not-yet-built project. **All design decisions are made**
(via a grilling session). Your job is to **implement** it. Read this top to bottom, then read
`CONTEXT.md` and `docs/adr/*` before writing code. Do not re-litigate settled decisions; if
something is genuinely ambiguous, ask the user.

## What this is

An interactive **study app for Awakening Valkyrie in Black Desert Online** — a faithful
rendering of the *Valkyrie Guide 2026* spreadsheet, enriched with BDO Valkyrie Discord
material. **Awakening only** — all Succession content is out of scope.

It is modeled on the sibling app at **`C:\Users\kevin\projects\maegu`** — copy its *engineering
skeleton* (static Vite + React + TypeScript; `data/*.json`; `sources/` ingestion; `scripts/`
build+validate; `CONTEXT.md` glossary; `docs/adr/`). Study these maegu files closely; you are
replicating their patterns:
- `maegu/data/abilities.json`, `combos.json`, `dps.json`, `setup.json` — data schemas
- `maegu/scripts/build_abilities.py`, `fetch_icons.py`, `validate_data.py`
- `maegu/research/bdocodex/parse_tooltips.py` + `raw/` — the Codex tooltip pull/parse flow
- `maegu/README.md` "Data refresh" section — the exact `curl bdocodex.com/tip.php?id=skill--<ID>` flow
- `maegu/app/src/` — pages (`AbilitiesPage`, `CombosPage`, `PracticePage`, `Rank1Page`),
  components (`ComboStrip`, `AbilityIcon`, `DpsTable`, `SourceImage`, `badges.tsx`, `Section`)

## Settled decisions (do not change without asking)

1. **Faithful-guide model, not maegu's practice model.** Data model follows the *guide's*
   shape (combos / add-ons / tricks / DPS). Combos stay fixed sequences with per-step
   protection badges — NOT reorganized into maegu's Movement/Protected/Unprotected sections.
   (ADR 0001)
2. **Skill Registry + protection from BDO Codex** (the spreadsheet has neither). `data/skills.json`
   is canonical; combos/DPS reference skill ids. Protection is the graded enum
   `iframe > super_armor > frontal_guard > none`, stored per-mode `pve`/`pvp`. (ADR 0002)
3. **Icon bridge:** the sheet's 44×44 combo icons are matched to Registry skills by **perceptual
   hash** against Codex icons; the Discord combos give an independent input↔skill cross-check.
   **Unmatched icons are flagged in data, never guessed.** (ADR 0002)
4. **Scope:** Awakening + only the pre-awakening skills that actually appear in awakening combos
   (tagged `kind: pre-awakening`, badged in UI). Never import the whole pre-awakening kit.
5. **PvP = AOS only**, drawn from BOTH the guide's 1v1 and Large-Scale content (Large-Scale leans
   on protected SA/FG play, which AOS rewards). Combos tagged `scale: 1v1 | large-scale`. No
   external AOS sourcing in v1; the real AOS deep-dive is post-v1 from R1 replays. (ADR 0003)
6. **Add-ons = screenshots only.** Do NOT transcribe add-on effect text (error-prone; maegu's
   hard-won stance). Show the source images.
7. **DPS values are LOCKED** — copy verbatim, never recompute. Preserve provenance.
8. **Practice = the combo strips themselves** (chrome-stripped, for a 2nd monitor). No quiz/drill.
9. **Theme:** maegu's dark-slate base + Valkyrie **gold/light-blue** accent.
10. **Source precedence:** when the spreadsheet and Discord disagree, **the spreadsheet wins**
    (most actively maintained). Discord enriches but defers on conflicts. Flag conflicts in data.
11. **No information loss.** `sources/` is lossless verbatim (text, images, anchors, comments,
    hyperlinks); `data/` is curved/normalized and references `sources/`. Normalization (e.g. the
    category enum) keeps the raw value too (`category_raw`). `scripts/validate_data.py` must
    enforce coverage and exit 0.

## Source material (all in `docs/`)

- `docs/Valkyrie Guide 2026.xlsx` — **the spreadsheet** (source of truth). 12 tabs; awakening-
  relevant: "Awakening (Combos, Add-ons)" (sheet4), "Awakening Tricks" (sheet5), "Awakening PvE
  DPS chart" (sheet6); supporting: Introduction, Important Info, Gearing Guide, Class Bug & Issues.
  Skip all Succession tabs + Change Log + Placeholder.
- `docs/discord-awakening-pve.md` — RoNNiE's PvE guide: per-skill metadata (importance, usage
  tags, recommended usage conditions), shortcodes, locked skills, quick-slot, rabams, swaps, BSR,
  and 3 PvE combos (Best DPS / Gyfin / DSR) as parallel input+skill sequences.
- `docs/discord-awakening-pvp.md` — Sarron's PvP guide: combo theory (Catches, Pre-buffs,
  De-buffs, Re-CCs, Payload, Down-Smash fishing, Purificatione timing), ~15 combos in families
  (Grab/Counter/Double-KD/Spear/Protected) with core variants, per-combo YouTube links, and 3
  modular Finishers. **Note:** user labeled it "pve" but content is PvP — it is correctly filed.

**`sources/skill-roster.md`** — **pre-built consolidated skill list** (every referenced skill
with canonical name, all shortcode aliases incl. the source's typos, `kind`, references, and
Discord metadata). This is the **input to Phase 1**: it turns "figure out the skills" into "fill
in `bdocodex_id` + `icon` for this list." It also lists the **non-skill tokens** (`:3hits:`,
`:1hit:`, `:ALLhits:`, emojis, `:sidestep:`) to NOT create entries for, and 5 open verification
items. Read it before Phase 1.

**Pre-extracted staging** (throwaway, but saves time) at:
- `C:\Users\kevin\Downloads\valk_extract\` — unzipped xlsx: `xl/media/` (131 images),
  `xl/worksheets/sheetN.xml`, `xl/drawings/drawingN.xml` (+ `_rels/`) for icon→cell anchors,
  `xl/comments1.xml` (sheet5 comments), hyperlinks in `xl/worksheets/_rels/sheetN.xml.rels`.
- `C:\Users\kevin\Downloads\valk_ingest\` — `text_dump.md` (full cell text, utf-8) and
  `image_anchors.json`. NOTE: openpyxl's image paths there are unreliable (all say image1.png);
  use the **drawing XML** (`xl/drawings/drawing4.xml` + its `.rels`) for the true icon→media map.
  `openpyxl` and `Pillow` are installed (Python 3.13). Console is cp1252 — set
  `PYTHONIOENCODING=utf-8` for any script that prints unicode.

Phase 0 should produce a proper `scripts/extract_xlsx.py` that regenerates `sources/` from
`docs/*.xlsx` (don't depend on the Downloads staging long-term).

## Data model (target schemas, mirror maegu)

`data/skills.json` — Registry. Per skill: `id` (kebab-case), `name`, `kind`
(`awakening`|`pre-awakening`), `shortcodes` (Discord `:Name:` aliases), `inputs`, `icon`,
`importance` (Discord 0–10, nullable), `usage_tags`, `recommended_usage` (Discord text),
`protection: { pve, pvp, tooltip_lines, notes, source, source_url, pulled }`, `description`
(Codex), `bdocodex_id`. Flag any skill whose sheet icon didn't phash-match.

`data/combos.json` — per combo: `id`, `mode` (`pve`|`pvp`), `scale` (`1v1`|`large-scale`, pvp
only), `protected` (bool), `family`, `core_variant` (nullable), `name`, `video` (url),
`steps: [{ skill, input, category, category_raw, optional, annotation }]`, `notes[]`, `sources[]`.
"or"/choice steps use `choices: [id…]` like maegu. Category enum: floating, transition,
crit-buff, ap-buff, re-cc, debuff, eva-debuff, dp-debuff, damage, engage, vacuum (+ raw kept).

`data/dps.json` — locked table rows: `skill` (id, flagged if unmatched), `name`, `hits`,
`damage`, `total`, `duration`, `dps`, plus header provenance (@RonnieBDO, 60% assumption,
"not frame exact").

`data/tricks.json` — cancels/macros: `id`, `name`, `sequences` (input steps w/ `➔`), `icons`,
`notes`, `comment` (from xlsx comments), `video`. ASCII-art blobs preserved in `sources/`,
rendered monospace or omitted (decorative, not data).

Add-on screenshots → `app/src/assets/addons/` (Sarron PvP, RoNNiE PvE), shown via a SourceImage
component. PvP combo-theory (Catches/Re-CCs/etc.) → a small `data/theory.json` or rendered from
the parsed Discord md.

## App / IA

Pages (React Router): **Skills** (searchable; toggle to group by protection tier; importance +
usage tags + recommended-usage shown) · **Combos** (sectioned PvE / PvP-AOS 1v1 / PvP Large-Scale;
protected vs unprotected; family + core-variant grouping; combo strips) · **Practice** (same strips,
chrome stripped) · **Add-ons** (screenshots) · **Tricks** · **DPS** (sortable, locked) ·
**Reference** (Introduction, Important Info, Gearing, Class Bugs — image galleries, not transcribed)
· **R1 AOS** (reserved empty route for future [[Observation]] data). **SA/FG/i-frame badges**
wherever a skill renders.

## Phases

- **Phase 0** — Scaffold (Vite/React/TS, dark-slate+gold, router, package.json like maegu) +
  `scripts/extract_xlsx.py` → lossless `sources/` + parse both Discord `.md` to intermediate.
- **Phase 1** — Registry: start from `sources/skill-roster.md`; find each skill's `bdocodex_id`,
  pull Codex tooltips (`research/bdocodex/raw/`), parse → `data/skills.json` with protection;
  `fetch_icons.py`; phash-bridge sheet icons → skill ids; flag unmatched. **Build a
  shortcode→id alias table that folds in every misspelling** from the roster (`Inpulsa`→divina-
  impulsa, `Promptess`→promptness, `Hastludium`→hastiludium, `PrimeSanctitasDeEnslar`→sanctitas-
  de-enslar, etc.) or Discord combos won't resolve. Work the roster's 5 open verification items.
- **Phase 2** — `data/combos.json`, `data/dps.json`, `data/tricks.json`; add-on screenshots into
  assets; `scripts/validate_data.py` (must exit 0). Two musts:
  - **Merge, don't duplicate, the PvE combos.** The sheet (icon strips + category labels) and the
    Discord (skill sequences) describe the *same* combos (Best DPS / Gyfin / DSR) from two angles
    — Discord supplies the skill identities the icons lack; sheet supplies categories and wins any
    order/content conflict (precedence). Produce ONE combo per combo, citing both sources, with a
    `conflicts[]` note where they diverge. Do not emit a sheet-combo and a Discord-combo separately.
  - **Hit-count tokens are annotations, not steps.** `:3hits:`/`:1hit:`/`:ALLhits:` modify the
    preceding skill (usually Sacrum Ferit) → put on that step as `annotation`/`hits`, never a step.
- **Phase 3** — App pages + components + badges + theme.
- **Phase 4** — Verify: headless smoke-render every route, `validate` exits 0, write `README.md`,
  `git init` + first commit, update the user's memory (`MEMORY.md`) with a valkyrie entry.

## Known gaps / future (reserved, not v1)

- **R1 AOS observation area** — user will capture Rank-1 replay notes later → drops into the
  reserved R1 route. Schema should not need rework.
- **More Discord** may be pasted later (e.g. PvP large-scale) — `sources/`→`data/` absorbs it.
- Some Discord screenshots/gifs were not pasted — acceptable.

## First steps for you

> **READ THIS FIRST — context-saving shortcut.** A prior instance already read the entire
> maegu reference tree (package.json, vite/tsconfig, all components, all pages, styles.css, the
> python scripts, the README data-refresh flow) AND fully extracted the valkyrie source facts
> (xlsx text dump, both Discord pastes, the staging dirs). All of it is **distilled into
> [`docs/IMPLEMENTATION-NOTES.md`](docs/IMPLEMENTATION-NOTES.md)** — the repo layout to build,
> the exact deps, every maegu code pattern to copy, the full per-skill protection/CC cross-check
> table, the locked DPS chart (verbatim with label→id mapping), the combo category labels+inputs,
> the tricks/add-ons inventory, and resolutions to all 5 roster open-verification items.
> **Do NOT re-read the maegu files or re-dump the xlsx** — that wastes context. Read
> IMPLEMENTATION-NOTES.md, this file, CONTEXT.md, the ADRs, and `sources/skill-roster.md`, then build.

1. Read `docs/IMPLEMENTATION-NOTES.md` (distilled maegu patterns + extracted source facts).
2. Read `CONTEXT.md`, `docs/adr/0001`–`0003`, `sources/skill-roster.md` (decisions + skill list).
3. Only open a specific maegu file if IMPLEMENTATION-NOTES.md leaves a real gap — don't bulk re-read.
4. **Phase 1 needs `bdocodex.com`** (skill tooltips + icons). You have the user's approval to access
   it — proceed. If a fetch fails, fall back to the sheet's "Important Info" protection/CC table
   (captured in IMPLEMENTATION-NOTES.md) and flag `protection.source` as the sheet, not Codex.
5. Work all phases to completion (Phase 0 → 4) autonomously; only stop on a genuine blocker.

### Status as of this handoff (updated 2026-06-15, prep pass 2)

A prep instance has now done all the **network/extraction discovery** AND the **mechanical
scaffold**, so the next instance can go straight to building data + app/src with almost no
research. **Read these first, in order, then build — do NOT open `C:\Users\kevin\projects\maegu`
and do NOT re-pull bdocodex or re-extract the xlsx:**
1. `docs/IMPLEMENTATION-NOTES.md` — distilled patterns + source facts (as before).
2. `docs/MAEGU-CODE-PATTERNS.md` — **NEW.** The reusable maegu component/data/script source
   inlined + Valkyrie adaptations (flat routing, category captions). Replaces reading the maegu repo.
3. `research/bdocodex/REGISTRY-DATA.md` — the curated Registry (ids, protection, tooltips, icons).
4. `research/bridge/combo_icon_map.md` — the sheet-icon → skill bridge (ADR 0002).
5. `research/bridge/addon_screenshots.md` — which source image is which add-on set.
6. `CONTEXT.md`, `docs/adr/0001–0003`, `sources/skill-roster.md` — decisions + skill list.

**DONE so far:**
- **Phase 0 scaffold (skeleton)** — `package.json`, `vite.config.ts`, `tsconfig.json`,
  `app/index.html`, `app/src/main.tsx`, `app/src/vite-env.d.ts`, `app/src/styles.css`
  (copied from maegu, **retinted to Valkyrie gold `--accent:#e8c060` + light-blue `--accent-2:#8fd8e0`**,
  mode-flip removed), `.gitignore`. `npm install` not yet run.
- **Phase 0 extraction** — `scripts/extract_xlsx.py` regenerates lossless `sources/` from the xlsx:
  `sources/text/<sheet>.md` (cell text), `sources/images/<sheet>/*.png` + `anchors.json`
  (419 images w/ cell anchors), `sources/comments.json`, `sources/hyperlinks.json` (32 links).
  DPS chart text verifies verbatim against the locked chart.
- **Phase 1 BDO Codex** — complete (next section).
- **Phase 1 icon→skill bridge (ADR 0002)** — `scripts/phash_bridge.py` + `research/bridge/`:
  21/24 combo-sheet icons matched at low Hamming distance; 3 flagged with best-guess candidates
  (Death Line Chase dist 20 ≈ certain; image4≈Divine Judgment of Light; image51 uncertain) for
  input-sequence cross-check. Revealed combos also use Celestial Spear / Divine Power / Severing Light.
- **Add-on screenshots identified** — `research/bridge/addon_screenshots.md`:
  `image132__B70` = Sarron PvP set, `image156__B99` = RoNNiE PvE set (both in
  `sources/images/awakening-combos-add-ons/`); banners are decorative.

- Staging (throwaway) still at `C:\Users\kevin\Downloads\valk_extract` and `valk_ingest`
  (no longer needed — `scripts/extract_xlsx.py` supersedes it).
- Console is cp1252 — set `PYTHONIOENCODING=utf-8` for any unicode-printing script.

**REMAINS (the next instance's job):** `data/skills.json` (via `scripts/build_skills.py`),
`data/combos.json` (merge sheet category-labels+inputs with Discord skill sequences — one combo
per combo, cite both, `conflicts[]` where they diverge; hit-tokens are annotations not steps),
`data/dps.json` (locked chart verbatim), `data/tricks.json`, `data/theory.json`; `scripts/`
`fetch_icons.py` + `validate_data.py` + `smoke.mjs` (shapes in MAEGU-CODE-PATTERNS.md); the
`app/src` data layer + types + components + pages (Skills/Combos/Practice/Add-ons/Tricks/DPS/
Reference/R1); then Phase 4 (validate exits 0, smoke-render every route, README, git init +
commit, MEMORY.md entry).

### ✅ Phase 1 — BDO Codex extraction COMPLETE (done 2026-06-15)

The hard, network-dependent part of Phase 1 is finished. All artifacts are in
`research/bdocodex/`. **The next instance should NOT re-do bdocodex discovery** — read
`research/bdocodex/REGISTRY-DATA.md` and build `data/skills.json` from it.

What was produced:
- **`research/bdocodex/REGISTRY-DATA.md`** ← START HERE for the registry. A curated table for
  all 34 referenced skills: `roster-id → bdocodex_id`, Codex name, input, cooldown, mp, the
  graded **protection enum per mode** (`prot pve`/`prot pvp`), and a curation note per skill.
  Plus the verbatim Codex protection_lines and the 12 locked-only skill IDs.
- **`research/bdocodex/tooltips.json`** — parsed tooltips for the 34 skills (name, description,
  input, required_level, mp_cost, cooldown, effects[], protection_lines[], icon_path).
- **`research/bdocodex/raw/skill-<ID>.html`** — the raw tip.php HTML (refresh source).
- **`research/bdocodex/icons/<bdocodex_id>.webp`** — 34 icons, 44×44, PIL-validated.
  `fetch_icons.py` (Phase 1 leftover task) should copy these → `app/src/assets/icons/<roster-id>.webp`.
- **`research/bdocodex/roster_id_map.json`** — `{roster-id: bdocodex_id}` (34 entries).
- **`research/bdocodex/protection_curated.json`** — `{roster-id: [pve, pvp, note]}` + locked-only map.
- **`research/bdocodex/valk_all_skills.txt`** — all 312 Valkyrie skills (id, name, icon path),
  the lookup table the IDs came from. **`skills_type7.json`** is its raw source (4.4 MB dump from
  `query.php?a=skills&l=us`, class column = "Valkyrie").
- **`research/bdocodex/parse_tooltips.py`** — the parser (run from `research/bdocodex/`).

How the IDs were chosen (so the next instance can trust/refresh them):
- bdocodex's per-class skill list is `https://bdocodex.com/query.php?a=skills&l=us` (one big JSON;
  column 4 = class name). The `skilltree` query is dead (returns empty) — use `a=skills`.
- Individual tooltips: `curl "https://bdocodex.com/tip.php?id=skill--<ID>&l=us" -o raw/skill-<ID>.html`.
- **Awakening** skills → highest base awakening tier (e.g. Sacrum Ferit IV=1966, Sanctitas de
  Enslar III=1977, Verdict IV=1971). **Pre-awakening** skills → the `Absolute:` (endgame) form
  where it exists (Severing Light=3200, Celestial Spear=3218, …); base max otherwise (Gladius
  Gloriae=1984, Shield Chase IV=4211). **Rabams** are single entries.
- Codex protection is authoritative (ADR 0002); it was cross-checked against the sheet "Important
  Info" table (in IMPLEMENTATION-NOTES) and **agrees on every skill** except two enrichments:
  Gladius Gloriae (Codex SA-before-hit vs sheet none → took Codex, flagged CONFLICT) and the two
  PvE-only-iframe movers Death Line Chase / Shield Chase (`pve=iframe, pvp=frontal_guard`).

Open verification items resolved by the pull:
- **#2** Divine Slam (2815, FG) and Divine Descent (2816, SA) are **distinct** adjacent skills,
  same input SHIFT+Z — keep both ids.
- **#3** PrimeSanctitasDeEnslar → single id `sanctitas-de-enslar` (bdocodex 1977); both shortcodes alias.
- **#4** `Guard` is a real Codex skill (718, Forward Guard stance); `sidestep` stays an input.
- **#1** add-on OCR labels confirmed (Sacrum Ferit / Hastiludium / Flow Divina Vult).
- Naming: bdocodex spells it **"Divina Inpulsa"** (6459) — keep roster id `divina-impulsa`, set
  display name to the Codex spelling, alias both.

What still remains in Phase 1 (for the next instance):
- Write `scripts/build_skills.py` (REGISTRY from REGISTRY-DATA.md + merge tooltips.json) → `data/skills.json`.
- Write `scripts/fetch_icons.py` (copy `research/bdocodex/icons/<bdocodex_id>.webp` →
  `app/src/assets/icons/<roster-id>.webp` using roster_id_map.json).
- Build the shortcode→id alias table (fold every roster typo) in `app/src/data`.
- The sheet-icon perceptual-hash bridge (ADR 0002) is still TODO — flag unmatched, never guess.
