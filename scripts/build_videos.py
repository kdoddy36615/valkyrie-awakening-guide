#!/usr/bin/env python3
"""Build data/videos.json — every video/link from the Discord guides + the spreadsheet,
grouped and cited by author. Deduped by URL (a link shown once on the page).

Pulls combo videos from combos.json and trick videos from tricks.json dynamically, then
adds the spreadsheet's hyperlinks (sources/hyperlinks.json) with curated labels/authors.

Run from repo root:  PYTHONIOENCODING=utf-8 python scripts/build_videos.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "videos.json"

GUIDE = "Valkyrie Guide 2026"

# Curated spreadsheet links (sources/hyperlinks.json) -> label / author / group.
# (sheet, cell): (label, url, author, group)
EXCEL = [
    # Cancels
    ("Verdict Cancel", "https://www.youtube.com/watch?v=3l1BtiU5NFA", GUIDE, "Cancels"),
    ("Gladius Gloriae Cancel", "https://youtu.be/p_02QjjhXJE", GUIDE, "Cancels"),
    ("Enslar Cancels", "https://youtu.be/RWjGa8nIXIw", GUIDE, "Cancels"),
    ("Vacuum Cancel", "https://streamable.com/871wo3", GUIDE, "Cancels"),
    ("Terra Sancta Cancel", "https://streamable.com/waz20q", GUIDE, "Cancels"),
    ("Terra Sancta — auto-cast BSR (hold RMB after Castigatio)", "https://streamable.com/nyis49", GUIDE, "Cancels"),
    ("Terra Sancta Cancel — Hold S+Q detail", "https://www.youtube.com/watch?v=RmjBIpwGBVo", GUIDE, "Cancels"),
    ("Celestial Smite Cancel", "https://streamable.com/cdnvh8", GUIDE, "Cancels"),
    # Transitions & movement
    ("Transition — Pre-awak Q + Space ➔ Q", "https://www.youtube.com/watch?v=6406zWPtMmc", GUIDE, "Transitions & Movement"),
    ("C-Swap Transition", "https://www.youtube.com/watch?v=8_Fr_YLD-8A", GUIDE, "Transitions & Movement"),
    ("Flurry of Kicks Transition", "https://www.youtube.com/watch?v=kRYN7_L3bKI", GUIDE, "Transitions & Movement"),
    ("Movement — Old School", "https://www.youtube.com/watch?v=Doth0keRt6w", GUIDE, "Transitions & Movement"),
    ("Movement — Shield Chase Dash", "https://www.youtube.com/watch?v=BmQEnGHDB2E", GUIDE, "Transitions & Movement"),
    ("Movement — Backwards DLC", "https://www.youtube.com/watch?v=eWR_bc2VNBk", GUIDE, "Transitions & Movement"),
    ("Movement — Promptness Walk", "https://www.youtube.com/watch?v=np4byv04PUQ", GUIDE, "Transitions & Movement"),
    ("Awakening Side-step", "https://streamable.com/3gopn8", GUIDE, "Transitions & Movement"),
    ("Crab Walk", "https://streamable.com/8fzlu1", GUIDE, "Transitions & Movement"),
    ("Pre-awakening Side-step", "https://streamable.com/3hd0ex", GUIDE, "Transitions & Movement"),
    # Combos from the sheet (Grab video dedupes against Sarron's; Knockdown is unique)
    ("GRAB combo", "https://www.youtube.com/watch?v=YH6vn2pSw44", GUIDE, "Combos (Guide)"),
    ("Knockdown (Core) combo", "https://www.youtube.com/watch?v=JPEH_UfmcKA", GUIDE, "Combos (Guide)"),
    # Gearing & reference
    ("Gearing Guide", "https://www.youtube.com/watch?v=frETWSVvFxM", GUIDE, "Gearing & Reference"),
    ("BDO Valkyrie Discord", "https://discord.gg/zKCbdy8Z8a", "Community", "Gearing & Reference"),
    # Class bug submissions (Skill Hit Delay & related)
    ("Skill Hit Delay", "https://www.youtube.com/watch?v=OsttiIyW0EM", "Shazar (EU)", "Class Bugs"),
    ("Skill Hit Delay", "https://www.youtube.com/watch?v=8vVeBdGyX8I", "Vesaia (EU)", "Class Bugs"),
    ("Skill Hit Delay (Lucem ➔ Promptness ➔ Purificatione)", "https://www.youtube.com/watch?v=SRHHV8s5Ppc", "Vesaia (EU)", "Class Bugs"),
    ("Skill Hit Delay (Blitz Stab)", "https://www.youtube.com/watch?v=YWA3Nk1kLe0", "ladladderson", "Class Bugs"),
    ("Skill Hit Delay (Divina Inpulsa out of Blitz Stab)", "https://www.youtube.com/watch?v=ODrCWLIyDfA", "Sarron (NA)", "Class Bugs"),
    ("Severing Light / Celestial Spear cast bug", "https://www.youtube.com/watch?v=WbRzc_-7Rqg", "RoNNiE (EU)", "Class Bugs"),
    ("Class bug clip", "https://www.youtube.com/watch?v=EGvcZG3_qkk", "RoNNiE (EU)", "Class Bugs"),
    ("Skill Hit Delay — official patch notes (June 2023)", "https://www.naeu.playblackdesert.com/en-US/News/Detail?groupContentNo=7147&countryType=en-US", "Pearl Abyss", "Class Bugs"),
]

GROUP_ORDER = ["PvP Combos", "PvE Combos", "Cancels", "Transitions & Movement",
               "Combos (Guide)", "Gearing & Reference", "Class Bugs"]
GROUP_NOTE = {
    "PvP Combos": "Per-combo demos from Sarron's PvP guide.",
    "Cancels": "Cancel demos from the spreadsheet's Tricks tab.",
    "Transitions & Movement": "Transition and movement clips from the Tricks tab.",
    "Combos (Guide)": "Combo demos linked from the spreadsheet.",
    "Gearing & Reference": "Gearing video and the community Discord.",
    "Class Bugs": "Community clips documenting the Skill Hit Delay and related bugs.",
}


import re

YT_RE = re.compile(r"(?:youtu\.be/|youtube\.com/watch\?v=)([\w-]+)")


def norm(url):
    """Dedupe key — collapse youtu.be/X and youtube.com/watch?v=X to the same id."""
    m = YT_RE.search(url)
    return f"yt:{m.group(1)}" if m else url


def load(name):
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def main():
    groups: dict[str, list] = {g: [] for g in GROUP_ORDER}
    seen = set()

    def add(group, label, url, author):
        key = norm(url)
        if key in seen:
            return False
        seen.add(key)
        groups.setdefault(group, []).append({"label": label, "url": url, "author": author})
        return True

    # Combo videos (Sarron = PvP, RoNNiE = PvE) — dynamic from combos.json
    for c in load("combos.json")["combos"]:
        if not c.get("video"):
            continue
        author = "Sarron" if c["mode"] == "pvp" else "RoNNiE"
        group = "PvP Combos" if c["mode"] == "pvp" else "PvE Combos"
        label = c["name"] + (f" — {c['core_variant']}" if c.get("core_variant") and c["core_variant"] not in c["name"] else "")
        add(group, label, c["video"], author)

    # Trick videos — dynamic from tricks.json
    for t in load("tricks.json")["tricks"]:
        if t.get("video"):
            add("Cancels", t["name"], t["video"], GUIDE)

    # Spreadsheet hyperlinks — curated
    for label, url, author, group in EXCEL:
        add(group, label, url, author)

    out_groups = []
    total = 0
    for g in GROUP_ORDER:
        vids = groups.get(g, [])
        if not vids:
            continue
        total += len(vids)
        out_groups.append({"title": g, "note": GROUP_NOTE.get(g, ""), "videos": vids})

    out = {
        "meta": {
            "note": "Every video/link from the Discord guides and the spreadsheet, cited by author. "
                    "Deduped by URL.",
            "count": total,
        },
        "groups": out_groups,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} — {total} links across {len(out_groups)} groups.")


if __name__ == "__main__":
    main()
