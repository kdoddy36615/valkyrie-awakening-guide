# Add-on screenshots & non-icon images — manifest (Phase 2/3 input)

The guide presents add-ons **as screenshots only** (ADR / HANDOFF §6 — never transcribed). These
were located by cross-referencing each big image's cell anchor against the resolved sheet text.
Copy the listed source images to `app/src/assets/addons/` and render via the `SourceImage` component.

Source: `sources/images/awakening-combos-add-ons/` (extracted by `scripts/extract_xlsx.py`).

## Add-on set screenshots (THE add-on content)

| source image | size | anchor | what it is | breakdown labels (from sheet text, NOT transcribed onto the image) |
|---|---|---|---|---|
| `image132__B70.png` | 850×635 | B70 | **Sarron's PvP add-on set** | Engage uptime (L74) · Reposition uptime (L78) · SA trade / largescale dmg (L82) · Crit + Down Modifiers (L86) — header "Add-ons breakdown:" L69 |
| `image156__B99.png` | 1100×753 | B99 | **RoNNiE's PvE add-on set** | Intuitive DP debuff stacking (M99) · Highest-priority DPS skill add-ons (M102) · Most important opener-skill add-ons (M108) · Spammable handy add-ons (M114) — header "Add-ons breakdown:" M98 |
| `image145__S21.png` | 487×342 | S21 | PvP combo-area screenshot (combo/finisher demo, in the 1v1 combo block rows ~16–27) — secondary; verify before using |

## Decorative / not data (skip)

- `image1__Q6.png`, `image98__B6.png` (442×131) — section-header banner art, repeated across sheets.
- Tricks sheet `image170__Q51.png` (211×253) — a BSR-macro / decorative graphic; the BSR macro is
  ASCII art in the sheet text (keep in `sources/`, render monospace or omit per HANDOFF).

## Other sheets' large images (reference galleries, not add-ons)

`sources/images/important-info/` and `gearing-guide/` contain larger figures (buff/debuff tables,
gear shots) used by the **Reference** page as image galleries — not transcribed (HANDOFF IA).
See each sheet's `anchors.json` for exact cell placement.
