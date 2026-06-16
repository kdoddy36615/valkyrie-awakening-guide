# Faithful-guide architecture, not maegu's practice model

The app is a **faithful rendering of the Valkyrie Guide 2026 spreadsheet**: the data model
follows the guide's own shape (combos, add-ons, tricks, DPS chart) rather than re-deriving an
opinionated domain model the way the sibling maegu app does. We deliberately borrow maegu's
*engineering skeleton* — static Vite + React + TS, `data/*.json`, `sources/` ingestion,
`scripts/` validation, `CONTEXT.md` glossary, `docs/adr/` — but **not** its protection-grouped
practice layout: combos stay the guide's fixed sequences (with per-step protection badges),
not Movement/Protected/Unprotected sections, because the guide's combos are taught sequences,
not freestyle priority play.

We chose this because there is a single authoritative content source (the spreadsheet) and the
goal is to make *that* usable, not to reconcile multiple sources into a new model. The cost: the
app's structure is dictated by the guide, so a future pivot to an opinionated model would be a
rewrite. Accepted as the right trade for v1; richer modeling can layer on later.
