# Valkyrie Awakening Guide

An interactive study app for **Awakening** Valkyrie in Black Desert Online, built as a
faithful rendering of the *Valkyrie Guide 2026* community spreadsheet. Scope is Awakening
only — all Succession material is out of scope. The app borrows the maegu app's engineering
skeleton (static Vite + React + TS, `data/*.json`, `sources/` ingestion, `scripts/`
validation) and follows the guide's own structure for its content (combos, add-ons, tricks,
DPS). It additionally adopts maegu's **protection model** as skill metadata — sourced from
BDO Codex (the spreadsheet has none) — but does *not* reorganize the guide's combos into
maegu's protection-grouped section layout.

## Language

### Sources

**Guide**:
The *Valkyrie Guide 2026* spreadsheet — the source of truth for guide *content* (combos,
add-ons, tricks, DPS chart). Extracted to `sources/`.
_Avoid_: sheet, doc (when referring to the canonical content)

**Source precedence**:
When the *Guide* (spreadsheet) and the *Discord info* disagree on a fact, **the Guide wins** —
it is the most actively maintained source. The Discord enriches (skill metadata, extra combos,
theory, videos) but defers to the Guide on any conflict. Both stay flagged with their dates;
conflicts are noted in the data, not silently resolved.

**Registry**:
The canonical list of Awakening Valkyrie skills (`data/skills.json`), sourced from **BDO
Codex** (names, icons, descriptions) the same way maegu builds `abilities.json`. Every
combo step, add-on row, and DPS row references a skill by its id. The Registry — not the
spreadsheet's pictures — owns skill identity.
_Avoid_: ability list (maegu's term; here a skill is a "Skill")

### Skills

**Skill**:
One Valkyrie skill that appears in awakening play, identified by a canonical kebab-case id
(e.g. `sanctitas-de-enslar`) carrying its display name, BDO Codex id, icon, inputs, and
`kind` (`awakening` | `pre-awakening`).
_Avoid_: ability (maegu's word), move, spell

**Pre-awakening skill**:
A non-awakening Valkyrie skill that the awakening combos still use as a transition or engage
(e.g. dashing backward drops you into the pre-awakening block). Only the pre-awakening skills
that actually appear in awakening combos enter the Registry — never the whole pre-awakening
kit — and they are badged in the UI so a combo's drop out of awakening is visible. Maegu calls
the analogous idea an "Absolute skill."
_Avoid_: preawk, absolute (maegu's term)

**Icon**:
A skill's 44×44 art. Authoritative icons come from BDO Codex; the spreadsheet's combo
icons are matched to Registry skills by perceptual hash (unmatched icons are flagged, not
guessed).

### Guide content

**Combo**:
An ordered sequence of skills with their inputs, rendered as a horizontal **combo strip**
(icon + category label + input key per step). Combos are split PvP and PvE.

**AOS**:
Arena of Solare — capped 3v3, the only PvP mode in scope. The *Guide* has no AOS-specific
combos, so AOS understanding is drawn from **both** PvP scales it does have — **1v1**
(grab/CC/burst) and **Large-Scale** (protected-ability emphasis). The dedicated AOS deep-dive
is post-v1, built from R1 replay [[Observation]]s.
_Avoid_: capped (alone), arena

**Large-Scale**:
The *Guide*'s group PvP content (100% BSR engage, heal rotation, finishers). Leans on
**protected (SA/FG) abilities**, which is exactly what AOS rewards — so it is an AOS-relevant
input, **not** out-of-scope. Tagged `scale: large-scale` (vs `1v1`) for filtering, but both
scales sit under PvP/AOS. Protection badges make its protected emphasis legible.
_Avoid_: node war, siege (those are the setting, not this label)

**Observation** _(planned, post-v1)_:
A logged record of watched gameplay — the Rank-1 AOS Valkyrie's skills and the order pressed
— kept as a usage record, **not** a taught combo. Will live on its own R1 AOS area. The
schema reserves room for this now; v1 ships without it.
_Avoid_: combo (an observation was played, not taught)

**Combo strip**:
The in-game-style rendering of a combo — a row of skill icons, each with the input above/
below and a category label. Mirrors maegu's combo strip.

**Protected / Unprotected combo**:
A combo-level property. Awakening combos are *inherently unprotected*; the PvP Discord keeps
a separate **Protected Combos** set built around `Guard` (FG) windows. Stored as `protected:
bool` on the combo. Protected combos are the AOS-relevant slice (capped 3v3 rewards protected
play) — distinct from per-skill [[Protection]].
_Avoid_: safe, guarded

**Combo family**:
A group of combos sharing an opener/situation (Grab, Counter / Ghost-float, Double-KD,
Celestial Spear, Protected). Each family has **core variants** — the same combo built on a
different core skill (`core_variant`: Sanctitas / Hastiludium / Castigatio). "Any core except
SacrumFerit" is a real constraint the source states.

**Catch**:
A PvP opener that locks the target (grab `Punishment`, `Counter`, `Celestial Spear`…) — the
start of a combo. _Avoid_: opener (use Catch; the source does)

**Re-CC**:
A skill used to re-apply crowd control mid-combo so the target stays down.

**Finisher**:
A modular combo tail (3 options in the source) appended to any combo ending in `BlitzStab`
[+ `DivinaInpulsa`]. Each finisher notes its own protection + reset potential.

**Category label**:
The role a step plays *in that combo* (FLOATING, TRANSITION, CRIT BUFF, AP BUFF, RE'CC,
DEBUFF, DAMAGE, ENGAGE, VACUUM, …). A property of the combo step's context, taken verbatim
from the guide.
_Avoid_: tag, type

**Hit-count modifier**:
A directive on how many hits of a skill to land before moving on (`1 hit`, `3 hits`, `all
hits` — usually on Sacrum Ferit). In the Discord it appears as a pseudo-shortcode
(`:3hits:`, `:1hit:`, `:ALLhits:`) but it is **not a skill** — it modifies the preceding
combo step. Stored on the step, never as its own step.
_Avoid_: counting these as skills

**Add-on set**:
A named, curated set of skill add-ons from a specific author (e.g. Sarron's PvP set,
RoNNiE's PvE set). Presented **as the source screenshots** — not transcribed and not
linked to the Registry — because add-on transcriptions are error-prone and untrusted (the
same stance maegu reached). The guide states add-ons are preference-based, so a set is one
author's recommendation, not canonical truth.
_Avoid_: build, addon-config

**Trick**:
A technique from the Awakening Tricks tab — mostly skill **cancels** (Verdict Cancel,
Gladius Gloriae Cancel) plus macros/tips (BSR macro, Ebuff DLC).
_Avoid_: tech, combo (a trick is not a combo)

**DPS chart**:
The per-skill PvE damage table from the guide (tabular, no icons in source). Values are
copied verbatim and **locked** — never recomputed (provenance: @RonnieBDO, 60% assumption,
"not frame exact").

### Protection

Sourced from **BDO Codex** tooltips (the *Guide* has none), attached to each Registry skill
and shown as a badge wherever the skill renders (Skills page, combo strips, DPS rows). The
Skills page can group skills by tier. Adopted from maegu's protection model.

**Protection**:
What a skill shields you with while animating — a graded scale stored per mode (PvE/PvP):
`iframe` > `super_armor` > `frontal_guard` > `none`. Never a boolean.

**i-frame**:
Invincibility — ignores all hits. Full protection.
_Avoid_: invincible (in prose; tooltips may say "Invincible")

**Super Armor (SA)**:
Ignores CC but takes damage. Full protection tier alongside i-frame.

**Frontal Guard (FG)**:
Blocks hits from the front only. Partial protection — its own middle tier, written "FG".
In-game text may spell it "Forward Guard"; same thing.
_Avoid_: block

**Unprotected**:
No i-frame, no SA, no FG during the animation.
_Avoid_: naked, free

### Future sources _(reserved, post-v1)_

**Discord info**:
Awakening Valkyrie content pasted from the BDO Valkyrie Discord. The raw paste lives in
`docs/` (alongside the source spreadsheet — `docs/` holds original human-provided
artifacts); it is then ingested into `sources/` and reconciled into combos/tricks/tips with
a currency flag (uncertain currency, like maegu's Discord PvP material) — not locked truth.
The user provides this **before** the build begins. See also [[Observation]] for the R1 AOS
replay notes.
