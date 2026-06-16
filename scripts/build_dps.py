#!/usr/bin/env python3
"""Build data/dps.json from the LOCKED sheet DPS chart — verbatim, never recomputed.

Parses the lossless cell dump (sources/text/awakening-pve-dps-chart.md), which is a
flat `CELL\\tVALUE` listing of the "Awakening PvE DPS chart" sheet. Row n (2..33):
  A{n}=label  B{n}=hits  C{n}=damage  D{n}=total  E{n}=duration[s]  F{n}=dps
Each label maps to a Registry skill id (see LABEL_MAP); combination/cancel rows
keep their label and also list the secondary skill in `also`. Header provenance
(@RonnieBDO, 60% assumption, "not frame exact") is preserved.

Run from repo root:  PYTHONIOENCODING=utf-8 python scripts/build_dps.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "sources" / "text" / "awakening-pve-dps-chart.md"
OUT = ROOT / "data" / "dps.json"

# sheet label -> (skill id, also[])  — ids verified against data/skills.json by validate_data.py
LABEL_MAP = {
    "Purificatione cancel": ("purificatione", []),
    "Wave of Light cancel": ("wave-of-light", []),
    "Divina Vult": ("flow-divina-vult", []),
    "Gladius (magnus) cancel": ("gladius-gloriae", []),
    "Blitz Stab": ("blitz-stab", []),
    "Casti cancel": ("castigatio", []),
    "D. Judgement of Light I cancel": ("divine-judgment-of-light", []),
    "Sacrum III": ("sacrum-ferit", []),
    "Purificatione": ("purificatione", []),
    "Terra Sancta": ("terra-sancta", []),
    "Verdict Vult cancel": ("verdict-lancia-iustitiae", ["flow-divina-vult"]),
    "Sanctitas de Enslar Vult cancel": ("sanctitas-de-enslar", ["flow-divina-vult"]),
    "Verdict I": ("verdict-lancia-iustitiae", []),
    "Verdict full cast": ("verdict-lancia-iustitiae", []),
    "Lucem Fluxum": ("flow-lucem-fluxum", []),
    "Verdict II": ("verdict-lancia-iustitiae", []),
    "Promptess": ("promptness", []),  # sheet typo for Promptness
    "Sanctitas de Enslar BSR": ("sanctitas-de-enslar", []),
    "Sacrum 3 hits": ("sacrum-ferit", []),
    "Celestial Smite + abs. spear": ("celestial-smite", ["celestial-spear"]),
    "Casti": ("castigatio", []),
    "Sanctitas de Enslar": ("sanctitas-de-enslar", []),
    "Severing Light": ("severing-light", []),
    "Divina Impulsa II": ("divina-impulsa", []),
    "Divine Judgement of Light full": ("divine-judgment-of-light", []),
    "Counter + S.Throw cancel": ("counter", ["shield-throw"]),
    "Sacrum I / II": ("sacrum-ferit", []),
    "Celestial Smite": ("celestial-smite", []),
    "Divina Impulsa full": ("divina-impulsa", []),
    "Hasti cancel": ("hastiludium", []),
    "Hasti": ("hastiludium", []),
    "Divina Impulsa I": ("divina-impulsa", []),
}


def parse_cells():
    cells = {}
    cell_re = re.compile(r"^([A-Z]+)(\d+)\t(.*)$")
    for line in SRC.read_text(encoding="utf-8").splitlines():
        m = cell_re.match(line)
        if m:
            cells[m.group(1) + m.group(2)] = m.group(3)
    return cells


def num(v):
    if v is None or v == "":
        return None
    try:
        f = float(v)
    except ValueError:
        return None
    return int(f) if f == int(f) else f


def main():
    cells = parse_cells()
    rows = []
    unknown = []
    for n in range(2, 34):  # data rows A2..A33
        label = cells.get(f"A{n}")
        if not label:
            continue
        mapped = LABEL_MAP.get(label)
        if mapped is None:
            unknown.append(label)
            sid, also = None, []
        else:
            sid, also = mapped
        rows.append({
            "skill": sid,
            "name": label,
            "also": also,
            "hits": num(cells.get(f"B{n}")),
            "damage": num(cells.get(f"C{n}")),
            "total": num(cells.get(f"D{n}")),
            "duration": num(cells.get(f"E{n}")),
            "dps": num(cells.get(f"F{n}")),
        })

    if unknown:
        print("UNMAPPED DPS labels:", file=sys.stderr)
        for u in unknown:
            print("  -", u, file=sys.stderr)
        sys.exit(1)

    out = {
        "meta": {
            "title": "Awakening PvE DPS chart",
            "source": "Valkyrie Guide 2026 — sheet \"Awakening PvE DPS chart\"",
            "author": cells.get("H3", "Made by @RonnieBDO"),
            "assumption": cells.get("A1", "60%") + " (DP/AP assumption header)",
            "notes": [cells.get("H6", "Values are not frame exact"),
                      cells.get("H7", "But they are more or less accurate")],
            "locked": True,
            "locked_note": "Values copied verbatim from the guide and never recomputed (ADR / HANDOFF §7).",
            "columns": ["skill", "name", "hits", "damage", "total", "duration", "dps"],
        },
        "rows": rows,
    }
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(rows)} locked DPS rows.")


if __name__ == "__main__":
    main()
