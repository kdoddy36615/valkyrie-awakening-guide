#!/usr/bin/env python3
"""Validate data/*.json referential integrity. Must exit 0 (HANDOFF Phase 4).

Loads data/skills.json -> IDS, then walks combos / dps / tricks / theory
recursively. Any value under an id-bearing field (skill, skills, choices, icons,
also) must resolve to a known Registry id (null is allowed for flagged-unmatched).
Also runs a few structural / coverage checks. Prints OK and exits 0 on success;
exits 1 with messages otherwise.

Run from repo root:  PYTHONIOENCODING=utf-8 python scripts/validate_data.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ID_FIELDS = {"skill", "skills", "choices", "icons", "also", "skill_refs"}
PROT_ENUM = {"iframe", "super_armor", "frontal_guard", "none"}


def load(name):
    with open(DATA / name, encoding="utf-8") as f:
        return json.load(f)


def collect_refs(obj, where, refs):
    """Walk obj; record (id, where) for every value under an ID_FIELD."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ID_FIELDS:
                if isinstance(v, str) or v is None:
                    refs.append((v, f"{where}.{k}"))
                elif isinstance(v, list):
                    for i, item in enumerate(v):
                        if isinstance(item, str) or item is None:
                            refs.append((item, f"{where}.{k}[{i}]"))
                        else:
                            collect_refs(item, f"{where}.{k}[{i}]", refs)
                else:
                    collect_refs(v, f"{where}.{k}", refs)
            else:
                collect_refs(v, f"{where}.{k}", refs)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            collect_refs(item, f"{where}[{i}]", refs)


def main():
    errors = []

    skills_file = load("skills.json")
    skills = skills_file["skills"]
    ids = {s["id"] for s in skills}

    # --- skills self-checks ---
    seen = set()
    alias = {}
    for s in skills:
        if s["id"] in seen:
            errors.append(f"skills: duplicate id {s['id']}")
        seen.add(s["id"])
        prot = s.get("protection")
        if prot is not None:
            for mode in ("pve", "pvp"):
                if prot.get(mode) not in PROT_ENUM:
                    errors.append(f"skills: {s['id']} protection.{mode} invalid: {prot.get(mode)}")
        for code in s.get("shortcodes", []):
            key = code.lower()
            if key in alias and alias[key] != s["id"]:
                errors.append(f"skills: shortcode {code} maps to both {alias[key]} and {s['id']}")
            alias[key] = s["id"]
        if not s.get("icon"):
            errors.append(f"skills: {s['id']} has no icon")

    # --- referential checks across the other data files ---
    refs = []
    for name in ("combos.json", "dps.json", "tricks.json", "theory.json"):
        data = load(name)
        collect_refs(data, name, refs)

    for sid, where in refs:
        if sid is None:
            continue  # null allowed (flagged-unmatched)
        if sid not in ids:
            errors.append(f"unknown skill id '{sid}' at {where}")

    # --- coverage: every awakening skill referenced somewhere is fine; report counts ---
    combos = load("combos.json")["combos"]
    dps = load("dps.json")["rows"]
    referenced = {sid for sid, _ in refs if sid}
    awakening = {s["id"] for s in skills if s["kind"] in ("awakening", "pre-awakening", "rabam")}
    orphan = sorted(awakening - referenced)

    if errors:
        print("VALIDATION FAILED:", file=sys.stderr)
        for e in errors:
            print("  -", e, file=sys.stderr)
        sys.exit(1)

    icon_dir = ROOT / "app" / "src" / "assets" / "icons"
    have_icons = {p.stem for p in icon_dir.glob("*.webp")} if icon_dir.exists() else set()
    missing_icons = sorted(ids - have_icons)

    print("OK — data is referentially consistent.")
    print(f"  skills:  {len(skills)}  (aliases: {len(alias)})")
    print(f"  combos:  {len(combos)}")
    print(f"  dps rows:{len(dps)}")
    print(f"  refs checked: {len(refs)}")
    if missing_icons:
        print(f"  NOTE: {len(missing_icons)} skills missing icon files "
              f"(run scripts/fetch_icons.py): {missing_icons}")
    if orphan:
        print(f"  NOTE: {len(orphan)} kit skills not referenced in any combo/dps "
              f"(expected for catch/utility skills): {orphan}")
    sys.exit(0)


if __name__ == "__main__":
    main()
