"""Perceptual-hash bridge (ADR 0002): identify the spreadsheet's 44x44 combo-strip icons by
hashing them against the BDO Codex Valkyrie icons (dHash + aHash, small Hamming threshold).

Reference set = ALL distinct Valkyrie icons (research/bdocodex/icons_all/, keyed by the icon
filename), so every combo icon resolves to a Codex skill *name*; we then annotate the Registry
`roster_id` when that skill is one of the 34 referenced skills. Same game art on both sides, so
matching is reliable; anything above threshold is FLAGGED, never guessed. Output:

  research/bridge/icon_bridge.json   media -> {skill_name, roster_id, distance, matched, cells, candidates}
  research/bridge/combo_icon_map.md  human-readable per-sheet table

Run with PYTHONIOENCODING=utf-8. Pillow only.
"""
import json
import re
from collections import defaultdict
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
ICONS_ALL = ROOT / "research" / "bdocodex" / "icons_all"
ID_MAP = json.loads((ROOT / "research" / "bdocodex" / "roster_id_map.json").read_text())
OUT = ROOT / "research" / "bridge"
SHEETS = ["awakening-combos-add-ons", "awakening-tricks", "important-info"]
THRESHOLD = 16  # max combined Hamming distance to accept a match


def dhash(img, size=16):
    g = img.convert("L").resize((size + 1, size), Image.LANCZOS)
    px = list(g.getdata())
    bits = 0
    for r in range(size):
        for c in range(size):
            bits = (bits << 1) | (1 if px[r * (size + 1) + c] > px[r * (size + 1) + c + 1] else 0)
    return bits


def ahash(img, size=16):
    g = img.convert("L").resize((size, size), Image.LANCZOS)
    px = list(g.getdata())
    avg = sum(px) / len(px)
    bits = 0
    for p in px:
        bits = (bits << 1) | (1 if p > avg else 0)
    return bits


def ham(a, b):
    return bin(a ^ b).count("1")


def sig(path):
    im = Image.open(path).convert("RGBA").resize((44, 44), Image.LANCZOS)
    bg = Image.new("RGBA", im.size, (0, 0, 0, 255))
    im = Image.alpha_composite(bg, im)
    return dhash(im), ahash(im)


def load_icon_meta():
    """icon filename -> {skills:[names], sids:[], roster_id}."""
    sid_to_rid = {str(v): k for k, v in ID_MAP.items()}
    meta = defaultdict(lambda: {"skills": [], "sids": [], "roster_id": None})
    for line in (ROOT / "research" / "bdocodex" / "valk_all_skills.txt").read_text(
            encoding="utf-8").splitlines():
        if not line.strip():
            continue
        sid, nm, ic = line.split("\t")
        if not ic:
            continue
        fn = ic.split("/")[-1]
        m = meta[fn]
        m["skills"].append(nm)
        m["sids"].append(sid)
        if sid in sid_to_rid:
            m["roster_id"] = sid_to_rid[sid]
    return meta


def main():
    meta = load_icon_meta()
    ref = {}  # icon filename -> (dhash, ahash)
    for f in ICONS_ALL.glob("*.webp"):
        ref[f.name] = sig(f)

    OUT.mkdir(parents=True, exist_ok=True)
    bridge = {}
    md = ["# Combo-icon -> skill bridge (perceptual hash, full Valkyrie icon set)\n",
          f"Reference icons: {len(ref)}. Threshold (dHash+aHash Hamming): {THRESHOLD}.",
          "`roster_id` set when the matched skill is one of the 34 Registry skills.",
          "Unmatched (over threshold) = flagged, never guessed.\n"]

    for sheet in SHEETS:
        sdir = ROOT / "sources" / "images" / sheet
        if not sdir.exists():
            continue
        by_media = defaultdict(list)
        for f in sdir.glob("*.png"):
            w, h = Image.open(f).size
            if 36 <= w <= 50 and 36 <= h <= 50:
                base = re.match(r"(image\d+)__", f.name)
                by_media[base.group(1) if base else f.stem].append(f)

        md.append(f"\n## {sheet}  ({len(by_media)} distinct icon media)\n")
        md.append("| media | cells | skill (Codex) | roster_id | dist | matched |")
        md.append("|---|---|---|---|---|---|")
        for media in sorted(by_media, key=lambda m: int(re.sub(r"\D", "", m) or 0)):
            files = sorted(by_media[media])
            d, a = sig(files[0])
            ranked = sorted((ham(d, rd) + ham(a, ra), fn) for fn, (rd, ra) in ref.items())
            best_dist, best_fn = ranked[0]
            matched = best_dist <= THRESHOLD
            m = meta.get(best_fn, {"skills": [], "roster_id": None})
            name = m["skills"][0] if m["skills"] else best_fn
            cells = [re.search(r"__([A-Z]+\d+)\.png", f.name).group(1) for f in files]
            bridge[f"{sheet}/{media}"] = {
                "skill_name": name if matched else None,
                "roster_id": m["roster_id"] if matched else None,
                "icon_file": best_fn if matched else None,
                "distance": best_dist,
                "matched": matched,
                "cells": cells,
                "candidates": [{"icon": fn, "skill": (meta.get(fn, {}).get("skills") or [fn])[0],
                                "distance": dd} for dd, fn in ranked[:3]],
            }
            md.append(f"| {media} | {','.join(cells[:6])}{'…' if len(cells) > 6 else ''} "
                      f"| {name if matched else '**UNMATCHED**'} | {m['roster_id'] or '—'} "
                      f"| {best_dist} | {'yes' if matched else 'no'} |")

    (OUT / "icon_bridge.json").write_text(json.dumps(bridge, indent=2, ensure_ascii=False),
                                          encoding="utf-8")
    (OUT / "combo_icon_map.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    total = len(bridge)
    matched = sum(1 for v in bridge.values() if v["matched"])
    combos = {k: v for k, v in bridge.items() if k.startswith("awakening-combos")}
    cm = sum(1 for v in combos.values() if v["matched"])
    print(f"bridged {matched}/{total} distinct icon media (threshold {THRESHOLD})")
    print(f"combos sheet: {cm}/{len(combos)} matched")
    for k, v in combos.items():
        if not v["matched"]:
            print(f"  UNMATCHED {k} cells={v['cells'][:4]} nearest={v['candidates'][0]}")


if __name__ == "__main__":
    main()
