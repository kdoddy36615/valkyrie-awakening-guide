# Skill identity and protection come from BDO Codex, bridged to the sheet by perceptual hash

Skill **identity** (names, ids, icons, descriptions) and **protection** (`iframe >
super_armor > frontal_guard > none`, stored per-mode `pve`/`pvp`, per maegu's ADR 0002) are
sourced from **BDO Codex tooltips**, not from the spreadsheet — the spreadsheet's combo cells
are only icon images and have no protection data at all. The Codex-built `data/skills.json` is
the canonical Registry; every combo step, DPS row, and pre-awakening reference points at a
skill id.

The combo strips in the sheet are bridged to the Registry by **perceptual-hash matching** the
sheet's 44×44 combo icons against the Codex icons (same game art, so matching is reliable).
Unmatched icons are **flagged in the data, never guessed**. Only the pre-awakening skills that
actually appear in awakening combos enter the Registry (tagged `kind: pre-awakening`), never
the whole pre-awakening kit.

Considered and rejected: deriving skill identity from the sheet's add-on/DPS text alone (loses
protection, fragile naming) and treating combo icons as opaque images (kills cross-linking,
search, and badges — the whole reason the Registry exists). Consequence: protection values are
patch-sensitive and must be re-reviewed when Codex tooltips are refreshed.
