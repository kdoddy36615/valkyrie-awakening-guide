#!/usr/bin/env python3
"""Build data/reference.json — the figure galleries for the Reference page.

The Reference sheets (Introduction, Important Info, Gearing, Class Bugs) are shown
as image galleries, not transcribed (HANDOFF IA). This scans each sheet's extracted
image folder, keeps the real figures (max dimension >= 250px), and drops the
repeated 442x131 section-banner art. Paths are relative to repo root so the
SourceImage component can resolve them.

Run from repo root:  PYTHONIOENCODING=utf-8 python scripts/build_reference.py
"""
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "sources" / "images"
OUT = ROOT / "data" / "reference.json"

SHEETS = [
    ("introduction", "Introduction", "State of Valkyrie in 2026, contents, and overview figures."),
    ("important-info", "Important Info", "Protection, CC, and buff/debuff reference (also reflected on the Skills page)."),
    ("gearing-guide", "Gearing Guide", "Recommended gear, crystals, and progression figures."),
    ("class-bug-issues", "Class Bug & Issues", "Known class bugs (notably the June 2023 Skill Hit Delay)."),
]

MIN_DIM = 250
BANNER = (442, 131)  # repeated decorative section header art


def main():
    out = {"meta": {"note": "Reference figure galleries — source screenshots, not transcribed."},
           "sheets": []}
    for key, title, desc in SHEETS:
        d = IMG / key
        figures = []
        if d.exists():
            for p in sorted(d.glob("*.png"), key=lambda x: x.name):
                try:
                    w, h = Image.open(p).size
                except Exception:
                    continue
                if (w, h) == BANNER:
                    continue
                if max(w, h) < MIN_DIM:
                    continue
                figures.append({"path": f"sources/images/{key}/{p.name}", "w": w, "h": h})
        out["sheets"].append({"key": key, "title": title, "desc": desc, "figures": figures})
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    total = sum(len(s["figures"]) for s in out["sheets"])
    print(f"Wrote {OUT.relative_to(ROOT)} — {total} figures across {len(SHEETS)} sheets.")


if __name__ == "__main__":
    main()
