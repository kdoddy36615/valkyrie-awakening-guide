#!/usr/bin/env python3
"""Copy skill icons into the app, named by canonical roster id.

The hard pull is already done — all icons live under research/bdocodex/:
  - icons/<bdocodex_id>.webp   : the 34 referenced skills (validated 44x44)
  - icons_all/<basename>.webp  : the full Valkyrie set (used for locked-only skills)

This script copies each skill's icon to app/src/assets/icons/<roster-id>.webp so
AbilityIcon (import.meta.glob) can resolve it. It also copies the add-on
screenshots into app/src/assets/addons/. No network needed.

Run from repo root:  python scripts/fetch_icons.py
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BDO = ROOT / "research" / "bdocodex"
ICONS_SRC = BDO / "icons"
ICONS_ALL = BDO / "icons_all"
DEST = ROOT / "app" / "src" / "assets" / "icons"
ADDON_DEST = ROOT / "app" / "src" / "assets" / "addons"
SKILLS = ROOT / "data" / "skills.json"
ALL_LIST = BDO / "valk_all_skills.txt"

# Add-on screenshots (research/bridge/addon_screenshots.md) -> friendly names.
ADDONS = {
    "awakening-combos-add-ons/image132__B70.png": "sarron-pvp.png",
    "awakening-combos-add-ons/image156__B99.png": "ronnie-pve.png",
    "awakening-combos-add-ons/image145__S21.png": "pvp-combo-demo.png",
}


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def build_all_icon_index():
    """bdocodex_id -> icon basename, parsed from valk_all_skills.txt (id\\tname\\tpath)."""
    idx = {}
    with open(ALL_LIST, encoding="utf-8") as f:
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 3:
                continue
            sid, _name, path = parts[0], parts[1], parts[2]
            base = path.rsplit("/", 1)[-1]
            idx[sid] = base
    return idx


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    ADDON_DEST.mkdir(parents=True, exist_ok=True)
    skills = load(SKILLS)["skills"]
    all_idx = build_all_icon_index()

    copied = 0
    missing = []
    for s in skills:
        rid = s["id"]
        bid = s.get("bdocodex_id")
        dest = DEST / f"{rid}.webp"
        if dest.exists():
            copied += 1
            continue
        # 1) referenced skills: research/bdocodex/icons/<bid>.webp
        src = ICONS_SRC / f"{bid}.webp"
        # 2) fall back to the full set via the id->basename index (locked-only)
        if not src.exists():
            base = all_idx.get(str(bid))
            src = ICONS_ALL / base if base else None
        if src and src.exists():
            shutil.copyfile(src, dest)
            copied += 1
        else:
            missing.append(f"{rid} (bdocodex {bid})")

    # Add-on screenshots
    addon_copied = 0
    for rel, name in ADDONS.items():
        src = ROOT / "sources" / "images" / rel
        if src.exists():
            shutil.copyfile(src, ADDON_DEST / name)
            addon_copied += 1
        else:
            missing.append(f"addon {rel}")

    print(f"Icons in {DEST.relative_to(ROOT)}: {copied}/{len(skills)} skills.")
    print(f"Add-on screenshots in {ADDON_DEST.relative_to(ROOT)}: {addon_copied}/{len(ADDONS)}.")
    if missing:
        print("MISSING:", file=sys.stderr)
        for m in missing:
            print("  -", m, file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
