# Awakening Valkyrie Guide

An interactive study app for **Awakening Valkyrie in Black Desert Online** — a faithful rendering
of the *Valkyrie Guide 2026* community spreadsheet, enriched with the BDO Valkyrie Discord
material and BDO Codex skill data. **Awakening only**; all Succession content is out of scope.

Static **Vite + React + TypeScript**. All content is built into `data/*.json` from the lossless
`sources/` extract and the curated `research/` pulls — no backend, no network at runtime.

## Quick start

```bash
npm install
npm run dev        # dev server (http://localhost:5173)
npm run build      # tsc --noEmit && vite build  ->  dist/
npm run preview    # serve the production build (http://localhost:4173)
npm run validate   # python scripts/validate_data.py  (referential integrity, must exit 0)
```

Smoke-render every route headlessly (needs a running `preview` or `dev` server + system Chrome/Edge):

```bash
node scripts/smoke.mjs            # against http://localhost:4173
```

## Pages

- **Skills** — the canonical Registry. Searchable; toggle to group by protection tier; shows
  importance, usage tags, recommended usage, cooldown/MP, and per-mode protection. Expand a row
  for the Codex description, effects, CC and the protection note.
- **Combos** — sectioned PvE / PvP-AOS 1v1 / PvP Large-Scale; family + core-variant grouping;
  protected badge; in-game-style combo strips (input + category + protection per step). Conflicts
  between sources are flagged.
- **Practice** — the same strips, chrome stripped, for a second monitor.
- **Add-ons** — source screenshots only (never transcribed).
- **Tricks** — skill cancels, weapon transitions, movement tech, macros.
- **DPS** — the locked PvE DPS chart, sortable, copied verbatim.
- **Reference** — PvP combo theory, quick-slot / lock lists, and the guide's intro / gearing /
  bug figures as image galleries.
- **R1 AOS** — reserved (empty) route for future Rank-1 replay observations.

## Data model

Canonical schema lives in `app/src/data/types.ts`. The Registry (`data/skills.json`) owns skill
identity; everything else references skills by id.

- `data/skills.json` — Registry: id, name, kind (`awakening` | `pre-awakening` | `rabam` |
  `quick-slot` | `locked-only`), shortcodes (incl. every Discord typo), inputs, icon, importance,
  usage tags, recommended usage, graded **protection** per mode (`iframe > super_armor >
  frontal_guard > none`), Codex description / cooldown / MP / effects / CC, `bdocodex_id`,
  `sheet_icon_matched`.
- `data/combos.json` — one combo per combo. PvE combos merge the sheet (category labels + inputs,
  skill identities confirmed by the icon phash bridge) with the Discord (skill names + usage);
  the sheet wins on conflicts (`conflicts[]`). Hit-count tokens are step **annotations**, not steps.
- `data/dps.json` — the locked DPS chart, verbatim, with provenance. Never recomputed.
- `data/tricks.json` — cancels / transitions / movement / macros.
- `data/theory.json` — PvP combo theory (catches, pre-buffs, de-buffs, re-CCs, payload, etc.).
- `data/reference.json` — figure-gallery manifest for the Reference page.

## Build pipeline (`scripts/`)

| script | output | notes |
|---|---|---|
| `extract_xlsx.py` | `sources/` | lossless extract of the xlsx (text, images + anchors, comments, hyperlinks) |
| `build_skills.py` | `data/skills.json` | curated REGISTRY + merge of `research/bdocodex/tooltips.json` + curated protection |
| `fetch_icons.py` | `app/src/assets/icons/`, `assets/addons/` | copies Codex icons (by roster id) + add-on screenshots |
| `build_combos.py` | `data/combos.json` | encodes every combo; merges sheet + Discord; resolves skill ids |
| `build_dps.py` | `data/dps.json` | parses the locked DPS cell-dump verbatim |
| `build_reference.py` | `data/reference.json` | selects the real figures (drops banner art / icons) |
| `validate_data.py` | — | referential integrity across all data; **exits 0** on success |
| `smoke.mjs` | `.screenshots/` | headless render of every route; fails on console errors / HTTP ≥ 400 / empty pages |

Regenerate all data after editing a builder:

```bash
PYTHONIOENCODING=utf-8 python scripts/build_skills.py
PYTHONIOENCODING=utf-8 python scripts/fetch_icons.py
PYTHONIOENCODING=utf-8 python scripts/build_combos.py
PYTHONIOENCODING=utf-8 python scripts/build_dps.py
PYTHONIOENCODING=utf-8 python scripts/build_reference.py
PYTHONIOENCODING=utf-8 python scripts/validate_data.py
```

(Set `PYTHONIOENCODING=utf-8` — the Windows console is cp1252 and the scripts print Unicode.)

## Data refresh (BDO Codex)

Protection values are patch-sensitive (ADR 0002). To refresh a skill's tooltip:

```bash
curl "https://bdocodex.com/tip.php?id=skill--<ID>&l=us" -o research/bdocodex/raw/skill-<ID>.html
python research/bdocodex/parse_tooltips.py     # rewrites tooltips.json
python scripts/build_skills.py                 # rebuild the Registry
```

The full Valkyrie skill list is `research/bdocodex/valk_all_skills.txt` (from
`query.php?a=skills&l=us`, class column "Valkyrie"). Roster-id → bdocodex-id map:
`research/bdocodex/roster_id_map.json`.

## Sources & precedence

- **Guide (spreadsheet)** — `docs/Valkyrie Guide 2026.xlsx`, source of truth for content. Wins on conflicts.
- **Discord** — RoNNiE (PvE) + Sarron (PvP); enriches but defers on conflicts (currency uncertain).
- **BDO Codex** — skill identity, icons, descriptions, and protection (the spreadsheet has none).

Design decisions are recorded in `CONTEXT.md` (glossary) and `docs/adr/0001–0003`.

## Scope notes

- Pre-awakening skills enter the Registry only when they appear in awakening combos.
- PvP = AOS (capped 3v3); drawn from the guide's 1v1 and Large-Scale content (ADR 0003).
- Add-ons are shown as screenshots, never transcribed (ADR / HANDOFF §6).
- DPS values are locked and copied verbatim (HANDOFF §7).
