"""Parse BDO Codex tip.php tooltip HTML (research/bdocodex/raw/skill-*.html) into
tooltips.json — one record per skill with name, description, input, costs, and the
effects block (which contains the protection lines). Run from research/bdocodex/.

Refresh raw files first (see README "Data refresh"):
  curl "https://bdocodex.com/tip.php?id=skill--<ID>&l=us" -o raw/skill-<ID>.html
"""
import glob
import html as htmllib
import json
import re


def clean(fragment: str) -> str:
    t = re.sub(r"<br\s*/?>", "\n", fragment)
    t = re.sub(r"<[^>]+>", "", t)
    t = htmllib.unescape(t)
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n ?", "\n", t)
    return t.strip()


records = {}
for path in sorted(glob.glob("raw/skill-*.html")):
    sid = int(re.search(r"skill-(\d+)", path).group(1))
    src = open(path, encoding="utf-8-sig", errors="replace").read()

    name_m = (re.search(r'tag_skill_name"><span[^>]*>([^<]+)', src)
              or re.search(r'tag_skill_name">([^<]+)', src)
              or re.search(r"<title>(.*?) - BDO Codex</title>", src))
    kr_m = re.search(r'id="item_name"><b><span[^>]*>([^<]+)', src)
    desc_m = re.search(r'tag_skill-description">(.*?)</span><hr', src, re.S)
    input_m = re.search(r'tag_control">(.*?)</span></td>', src, re.S)
    level_m = re.search(r'tag_required_level">(\d+)', src)
    points_m = re.search(r'tag_required_skill_points">(\d+)', src)
    mp_m = re.search(r'tag_required_mp">([^<]+)', src)
    cd_m = re.search(r'tag_cooldown">([^<]+)', src)
    effects_m = re.search(r'<div id="description">(.*?)</div>', src, re.S)

    effects_text = clean(effects_m.group(1)) if effects_m else ""
    effects = [ln.strip() for ln in effects_text.split("\n") if ln.strip()]
    protection = [ln for ln in effects
                  if re.search(r"Invincible|Super Armor|Forward Guard", ln)]

    # icon path used by fetch_icons.py
    icon_m = re.search(r'<img src="(/items/[^"]+\.webp)" alt="icon" width="40"', src)

    records[sid] = {
        "bdocodex_id": sid,
        "url": f"https://bdocodex.com/us/skill/{sid}/",
        "name": clean(name_m.group(1)) if name_m else None,
        "name_kr": clean(kr_m.group(1)) if kr_m else None,
        "description": clean(desc_m.group(1)) if desc_m else None,
        "input": clean(input_m.group(1)) if input_m else None,
        "required_level": int(level_m.group(1)) if level_m else None,
        "required_points": int(points_m.group(1)) if points_m else None,
        "mp_cost": clean(mp_m.group(1)) if mp_m else None,
        "cooldown": clean(cd_m.group(1)) if cd_m else None,
        "effects": effects,
        "protection_lines": protection,
        "icon_path": icon_m.group(1) if icon_m else None,
    }

with open("tooltips.json", "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False, indent=2)
print(f"wrote tooltips.json with {len(records)} skills")
