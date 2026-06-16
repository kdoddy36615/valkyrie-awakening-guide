#!/usr/bin/env python3
"""Build data/combos.json — one combo per combo, merging the sheet with the Discord.

Per HANDOFF Phase 2:
  - The sheet (icon strips + category labels + inputs) and the Discord (skill
    sequences) describe the SAME PvE combos (Best DPS / Gyfin / DSR). We emit ONE
    combo each, citing both sources, with conflicts[] where order/content diverge.
    The sheet wins on conflicts (source precedence, CONTEXT / HANDOFF §10).
  - Hit-count tokens (:3hits: / :1hit: / :ALLhits:) are step ANNOTATIONS on the
    preceding skill (Sacrum Ferit), never their own steps.
  - PvP combos come from the Discord families (Sarron) — the sheet's PvP is two
    generic 1v1 templates (GRAB / KNOCKDOWN-core) + Large-Scale, which we also
    include from the sheet. GRAB is merged with the Discord General Grab combo.

Step skills are Registry ids; validate_data.py checks every id resolves.
Run from repo root:  PYTHONIOENCODING=utf-8 python scripts/build_combos.py
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "data" / "skills.json"
OUT = ROOT / "data" / "combos.json"

# --- source citations ------------------------------------------------------
SHEET = {"source": "sheet", "ref": "Valkyrie Guide 2026 — sheet \"Awakening (Combos, Add-ons)\""}
PVE = {"source": "discord", "ref": "BDO Valkyrie Discord — RoNNiE PvE guide", "updated": "2025-02-23"}
PVP = {"source": "discord", "ref": "BDO Valkyrie Discord — Sarron PvP", "updated": "2025-03"}

# --- category normalization (verbatim raw kept on every step) --------------
CAT_NORM = {
    "AP BUFF": "ap-buff", "EVA DEBUFF": "eva-debuff", "DP DEBUFF": "dp-debuff",
    "CRIT BUFF": "crit-buff", "FLOATING": "floating", "TRANSITION": "transition",
    "RE'CC": "re-cc", "DEBUFF": "debuff", "DAMAGE": "damage", "ENGAGE": "engage",
    "VACUUM": "vacuum", "KNOCKDOWN": "knockdown", "100% BSR": "bsr",
}


def S(skill, inp, cat=None, opt=False, annot=None, phase=None):
    """One combo step."""
    return {
        "skill": skill,
        "input": inp,
        "category": CAT_NORM.get(cat) if cat else None,
        "category_raw": cat,
        "optional": opt,
        "annotation": annot,
        "phase": phase,
    }


# ===========================================================================
# PvE combos — merged (sheet skill identities confirmed via the phash bridge,
# Discord supplies the skill names + usage). Categories + inputs from the sheet.
# ===========================================================================
COMBOS = []

COMBOS.append({
    "id": "pve-best-dps", "mode": "pve", "scale": None, "protected": False,
    "family": "PvE", "core_variant": None, "name": "Best DPS Combo",
    "video": None,
    "steps": [
        S("sanctitas-de-enslar", "F", "AP BUFF"),
        S("flow-divina-vult", "LMB/F", "EVA DEBUFF"),
        S("castigatio", "S+LMB"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("blitz-stab", "W+RMB", "EVA DEBUFF"),
        S("divina-impulsa", "SHIFT+Q", "AP BUFF"),
        S("sacrum-ferit", "RMB", "CRIT BUFF"),
        S("flow-lucem-fluxum", "RMB (Flow)"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "S+RMB"),
        S("shield-chase", "SHIFT + Direction"),
        S("severing-light", "LMB+RMB", opt=True),
        S("gladius-gloriae", "F"),
        S("celestial-spear", "S+E", "CRIT BUFF", opt=True),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF"),
    ],
    "notes": [
        "Not loopable, moderate APM.",
        "The sheet marks the Severing Light and Celestial Spear steps OPTIONAL.",
        "Awakening is ~30% behind top-tier grinders PvE-wise; there are no loopable combos.",
    ],
    "sources": [SHEET, PVE],
    "conflicts": [
        "Step order 16-17: the Discord lists Gladius Gloriae (F) before Severing Light "
        "(LMB+RMB); the sheet lists Severing Light before Gladius Gloriae. The sheet wins "
        "(source precedence)."
    ],
})

COMBOS.append({
    "id": "pve-gyfin", "mode": "pve", "scale": None, "protected": False,
    "family": "PvE", "core_variant": None, "name": "Gyfin Combo",
    "video": None,
    "steps": [
        S("sanctitas-de-enslar", "F", "AP BUFF"),
        S("flow-divina-vult", "LMB/F", "EVA DEBUFF"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF"),
        S("castigatio", "S+LMB"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("blitz-stab", "W+RMB", "EVA DEBUFF"),
        S("hastiludium", "W+F"),
        S("divina-impulsa", "SHIFT+Q", "AP BUFF"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("sacrum-ferit", "RMB", "CRIT BUFF"),
    ],
    "notes": ["Open with a crit prebuff (Sacrum Ferit or Celestial Spear) before the combo."],
    "sources": [SHEET, PVE],
    "conflicts": [],
})

COMBOS.append({
    "id": "pve-dsr", "mode": "pve", "scale": None, "protected": False,
    "family": "PvE", "core_variant": None, "name": "Darkseekers (DSR) Combo",
    "video": None,
    "steps": [
        # --- Loop 1 ---
        S("hastiludium", "W+F", phase="Loop 1"),
        S("promptness", "SPACE", phase="Loop 1"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF", phase="Loop 1"),
        S("sanctitas-de-enslar", "F", "AP BUFF", phase="Loop 1"),
        S("flow-divina-vult", "LMB/F", "EVA DEBUFF", phase="Loop 1"),
        S("castigatio", "S+LMB", phase="Loop 1"),
        S("promptness", "SPACE", phase="Loop 1"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB", phase="Loop 1"),
        S("blitz-stab", "W+RMB", "EVA DEBUFF", phase="Loop 1"),
        S("divina-impulsa", "SHIFT+Q", "AP BUFF", phase="Loop 1"),
        S("sacrum-ferit", "RMB", "CRIT BUFF", phase="Loop 1"),
        S("flow-lucem-fluxum", "RMB (Flow)", phase="Loop 1"),
        S("promptness", "SPACE", phase="Loop 1"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF", phase="Loop 1"),
        S("castigatio", "S+LMB", phase="Loop 1"),
        # --- Loop 2 ---
        S("wave-of-light", "S+F", "DP DEBUFF", phase="Loop 2"),
        S("guard", "Q", phase="Loop 2"),
        S("sanctitas-de-enslar", "F", "AP BUFF", phase="Loop 2"),
        S("flow-divina-vult", "LMB/F", "EVA DEBUFF", phase="Loop 2"),
        S("castigatio", "S+LMB", phase="Loop 2"),
        S("death-line-chase", "SHIFT+W/S", phase="Loop 2"),
        S("promptness", "SPACE", phase="Loop 2"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB", phase="Loop 2"),
        S("death-line-chase", "SHIFT+W/S", phase="Loop 2"),
        S("death-line-chase", "SHIFT+W/S", phase="Loop 2"),
        S("promptness", "SPACE", phase="Loop 2"),
        S("purificatione", "SHIFT+LMB", "DP DEBUFF", phase="Loop 2"),
        S("blitz-stab", "W+RMB", "EVA DEBUFF", phase="Loop 2"),
        S("divina-impulsa", "SHIFT+Q", "AP BUFF", phase="Loop 2"),
        S("sacrum-ferit", "RMB", "CRIT BUFF", phase="Loop 2"),
        S("flow-lucem-fluxum", "RMB (Flow)", phase="Loop 2"),
        S("shield-chase", "SHIFT + Direction", phase="Loop 2"),
        S("gladius-gloriae", "F", "EVA DEBUFF", phase="Loop 2"),
        S("promptness", "SPACE", phase="Loop 2"),
        S("castigatio", "S+LMB", phase="Loop 2"),
        S("terra-sancta", "S+RMB", phase="Loop 2"),
    ],
    "notes": ["Darkseekers (DSR) two-loop rotation. Loop 2 drops out of awakening via "
              "Death Line Chase and the pre-awakening filler (Shield Chase / Gladius Gloriae)."],
    "sources": [SHEET, PVE],
    "conflicts": [],
})

# ===========================================================================
# PvP — sheet generic 1v1 templates + Large-Scale (sheet), Discord families.
# ===========================================================================

# GRAB — merged: sheet GRAB template + Discord General Grab combo.
COMBOS.append({
    "id": "pvp-grab-general", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Grab", "core_variant": "Any core except Sacrum Ferit",
    "name": "General Grab Combo", "video": "https://youtu.be/YH6vn2pSw44",
    "steps": [
        S("punishment", "E", "FLOATING"),
        S("promptness", "SPACE", "TRANSITION"),
        S("sacrum-ferit", "RMB", "CRIT BUFF", annot="3 hits"),
        S("divina-impulsa", "SHIFT+Q", "AP BUFF"),
        S("flow-lucem-fluxum", "Quick Slot", "RE'CC"),
        S("purificatione", "SHIFT+LMB", "DEBUFF"),
        S("castigatio", "S+LMB", "DAMAGE"),
        S("terra-sancta", "S+RMB", "DAMAGE"),
        S("blitz-stab", "W+RMB", "DAMAGE"),
    ],
    "notes": [],
    "sources": [SHEET, PVP],
    "conflicts": [
        "The Discord casts Terra Sancta by holding after Castigatio; the sheet lists its "
        "direct input S+RMB (used here, source precedence)."
    ],
})

# KNOCKDOWN (CORE ONLY) — sheet generic 1v1 template.
COMBOS.append({
    "id": "pvp-knockdown-core", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Knockdown", "core_variant": "Core (any except Sacrum Ferit)",
    "name": "Knockdown Combo (Core)", "video": None,
    "steps": [
        S("sanctitas-de-enslar", "F", "KNOCKDOWN"),
        S("sacrum-ferit", "A/D+RMB", "CRIT BUFF"),
        S("promptness", "SPACE", "TRANSITION"),
        S("divina-impulsa", "SHIFT+Q", "AP BUFF"),
        S("flow-lucem-fluxum", "Quick Slot", "RE'CC"),
        S("purificatione", "SHIFT+LMB", "DEBUFF"),
        S("castigatio", "S+LMB", "DAMAGE"),
        S("terra-sancta", "S+RMB", "DAMAGE"),
        S("blitz-stab", "W+RMB", "DAMAGE"),
    ],
    "notes": ["The sheet's generic core 1v1 template (core slot = any knockdown core "
              "except Sacrum Ferit). The Discord core families below build on it."],
    "sources": [SHEET],
    "conflicts": [],
})

# --- Discord GRAB variants ---
COMBOS.append({
    "id": "pvp-grab-hasti", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Grab", "core_variant": "Hastiludium",
    "name": "Grab Combo — Hastiludium variant", "video": "https://youtu.be/KEnce0yW1sM",
    "steps": [
        S("punishment", "E"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("sacrum-ferit", "A/D+RMB", annot="1 hit — side Sacrum cancels Divina Inpulsa's first hit"),
        S("divina-impulsa", "SHIFT+Q"),
        S("hastiludium", "W+F"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
    ],
    "notes": ["Uses side Sacrum Ferit to cancel the first hit of Divina Inpulsa."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-grab-enslar", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Grab", "core_variant": "Sanctitas de Enslar",
    "name": "Grab Combo — Enslar variant", "video": "https://youtu.be/gE5yCcQtpmI",
    "steps": [
        S("punishment", "E"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("guard", "Q"),
        S("sacrum-ferit", "RMB (hold)", annot="1-3 hits depending on casting speed"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F/LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
        S("divina-impulsa", "SHIFT+Q"),
    ],
    "notes": ["You can do 1-3 hits of Sacrum Ferit depending on casting speed."],
    "sources": [PVP], "conflicts": [],
})

# --- Core: Sanctitas de Enslar ---
COMBOS.append({
    "id": "pvp-enslar-general", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Sanctitas de Enslar", "core_variant": "General",
    "name": "General Enslar Combo", "video": "https://youtu.be/xKYext4FGD8",
    "steps": [
        S("sanctitas-de-enslar", "F"),
        S("sacrum-ferit", "A/D+RMB", annot="1 hit"),
        S("promptness", "SPACE"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("flow-divina-vult", "LMB", annot="Verdict cancel"),
        S("guard", "Q"),
        S("flow-lucem-fluxum", "Quick Slot"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
        S("divina-impulsa", "SHIFT+Q"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-enslar-divina-vult", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Sanctitas de Enslar", "core_variant": "Divina Vult",
    "name": "Enslar Combo — Divina Vult variant", "video": "https://youtu.be/qd7_Ig7JtiA",
    "steps": [
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "Hold (F/LMB after Sanctitas)"),
        S("promptness", "SPACE"),
        S("sacrum-ferit", "RMB", annot="all hits"),
        S("flow-lucem-fluxum", "Hold (RMB after Sacrum)"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
        S("divina-impulsa", "SHIFT+Q"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

# --- Core: Hastiludium ---
COMBOS.append({
    "id": "pvp-hasti-general", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Hastiludium", "core_variant": "General",
    "name": "General Hasti Combo", "video": "https://youtu.be/Wz97moUFPzY",
    "steps": [
        S("hastiludium", "W+F"),
        S("divina-impulsa", "SHIFT+Q"),
        S("promptness", "SPACE"),
        S("sacrum-ferit", "RMB", annot="all hits"),
        S("flow-lucem-fluxum", "Hold (RMB after Sacrum)"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-hasti-enslar", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Hastiludium", "core_variant": "Enslar",
    "name": "Hasti Combo — Enslar variant", "video": "https://youtu.be/OLOn3ZM_HyM",
    "steps": [
        S("hastiludium", "W+F"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "Hold (F/LMB after Sanctitas)"),
        S("promptness", "SPACE"),
        S("sacrum-ferit", "RMB", annot="1 hit"),
        S("flow-lucem-fluxum", "Quick Slot"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
        S("divina-impulsa", "SHIFT+Q"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

# --- Counter (Ghost float) ---
COMBOS.append({
    "id": "pvp-counter-ghost-float", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Counter", "core_variant": "Any core except Sacrum Ferit",
    "name": "Counter Combo (Ghost float)", "video": "https://youtu.be/FE63KInRJ6Y",
    "steps": [
        S("counter", "S+LMB", annot="then sidestep (A/D+RMB) to ghost-float"),
        S("promptness", "SPACE"),
        S("divina-impulsa", "SHIFT+Q"),
        S("sacrum-ferit", "RMB"),
        S("flow-lucem-fluxum", "Hold (RMB after Sacrum)"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
    ],
    "notes": ["The sidestep (A/D+RMB) is a movement input, not a skill."],
    "sources": [PVP], "conflicts": [],
})

# --- Double KD ---
COMBOS.append({
    "id": "pvp-doublekd-gladius", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Double KD", "core_variant": "Gladius Gloriae",
    "name": "Double KD — Gladius Gloriae variant", "video": "https://youtu.be/MxqRhKgsQ-o",
    "steps": [
        S("gladius-gloriae", "F"),
        S("promptness", "SPACE"),
        S("divina-impulsa", "SHIFT+Q"),
        S("guard", "Q"),
        S("sacrum-ferit", "RMB", annot="all hits"),
        S("flow-lucem-fluxum", "Hold (RMB after Sacrum)"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
    ],
    "notes": ["Any core except Sacrum Ferit."], "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-doublekd-blitz", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Double KD", "core_variant": "Blitz Stab",
    "name": "Double KD — Blitz Stab variant", "video": "https://youtu.be/cgJPsh3wabM",
    "steps": [
        S("blitz-stab", "W+RMB"),
        S("divina-impulsa", "SHIFT+Q"),
        S("promptness", "SPACE"),
        S("sacrum-ferit", "RMB", annot="all hits"),
        S("flow-lucem-fluxum", "Hold (RMB after Sacrum)"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("shield-chase", "SHIFT+A/D"),
        S("gladius-gloriae", "F"),
        S("celestial-spear", "S+E"),
        S("divine-judgment-of-light", "LMB"),
    ],
    "notes": ["Any core except Sacrum Ferit. You can replace Shield Chase + Gladius Gloriae "
              "with Divine Power + Flying Kick + Severing Light + Gladius Gloriae for more DMG."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-doublekd-lucem", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Double KD", "core_variant": "Flow: Lucem Fluxum",
    "name": "Double KD — Lucem Fluxum variant", "video": "https://youtu.be/-IwNG8OnoTo",
    "steps": [
        S("flow-lucem-fluxum", "Quick Slot"),
        S("purificatione", "SHIFT+LMB"),
        S("promptness", "SPACE"),
        S("divina-impulsa", "SHIFT+Q"),
        S("sacrum-ferit", "RMB"),
        S("blitz-stab", "W+RMB"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("flow-divina-vult", "LMB", annot="Verdict cancel"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("divine-power", "SHIFT+F"),
    ],
    "notes": ["Any core except Sacrum Ferit. Needs BSR Terra Sancta to start a down-smash chain."],
    "sources": [PVP], "conflicts": [],
})

# --- Celestial Spear ---
COMBOS.append({
    "id": "pvp-spear-general", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Celestial Spear", "core_variant": "General",
    "name": "General Spear Combo", "video": "https://youtu.be/fs9AydcuVkA",
    "steps": [
        S("celestial-spear", "S+E"),
        S("promptness", "SPACE"),
        S("divina-impulsa", "SHIFT+Q"),
        S("sacrum-ferit", "RMB"),
        S("flow-lucem-fluxum", "Hold (RMB after Sacrum)"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
    ],
    "notes": ["Any core except Sacrum Ferit. You can skip Sacrum Ferit if you fear missing "
              "the re-cc; Flow: Lucem Fluxum applies Sacrum's add-ons and Celestial Spear "
              "gives the crit-rate buff for nearly the whole combo."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-spear-hasti", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Celestial Spear", "core_variant": "Hastiludium",
    "name": "Spear Combo — Hasti variant", "video": "https://youtu.be/EsFS5qmpq5I",
    "steps": [
        S("celestial-spear", "S+E"),
        S("promptness", "SPACE"),
        S("divina-impulsa", "SHIFT+Q"),
        S("hastiludium", "W+F"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-spear-enslar", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Celestial Spear", "core_variant": "Sanctitas de Enslar",
    "name": "Spear Combo — Enslar variant", "video": "https://youtu.be/QRwKLKlA2bE",
    "steps": [
        S("celestial-spear", "S+E"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F/LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("blitz-stab", "W+RMB"),
        S("divina-impulsa", "SHIFT+Q"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

# --- Protected combos (built around Guard FG windows) ---
PROT_NOTE = ("Protected combos use: Terra Sancta > Guard > Verdict, or Flow: Divina Vult > "
             "Guard > Terra Sancta. Hold S+Q during Terra Sancta (S+RMB) or Flow: Divina Vult "
             "(F/LMB) to minimize the end delay without canceling hits — press S first. Cast "
             "Verdict from hotbar: spam the hotkey while holding S+Q and it casts on entering Guard.")

COMBOS.append({
    "id": "pvp-protected-general", "mode": "pvp", "scale": "1v1", "protected": True,
    "family": "Protected", "core_variant": "General",
    "name": "General Protected Combo", "video": "https://youtu.be/ACLHV3I_jKA",
    "steps": [
        S("punishment", "E"),
        S("promptness", "SPACE"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F/LMB"),
        S("death-line-chase", "SHIFT+S"),
        S("sacrum-ferit", "RMB"),
        S("guard", "Q"),
        S("flow-lucem-fluxum", "Quick Slot"),
        S("purificatione", "SHIFT+LMB"),
        S("terra-sancta", "S+RMB"),
        S("guard", "Q (S+Q)"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("flow-divina-vult", "LMB", annot="Verdict cancel"),
    ],
    "notes": ["Any core except Sanctitas de Enslar or Sacrum Ferit."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-protected-enslar", "mode": "pvp", "scale": "1v1", "protected": True,
    "family": "Protected", "core_variant": "Sanctitas de Enslar",
    "name": "Protected Combo — Enslar variant", "video": "https://youtu.be/Eg3_scnlhF4",
    "steps": [
        S("punishment", "E"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("sacrum-ferit", "A/D+RMB", annot="1 hit"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F/LMB"),
        S("guard", "Q (S+Q)"),
        S("terra-sancta", "S+RMB"),
        S("guard", "Q (S+Q)"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("flow-divina-vult", "LMB", annot="Verdict cancel"),
    ],
    "notes": ["Feel free to cancel all hits of Sacrum Ferit with Guard for a shorter frontal "
              "guard. You'll get the crit buff regardless, but your add-ons won't apply."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-protected-hasti", "mode": "pvp", "scale": "1v1", "protected": True,
    "family": "Protected", "core_variant": "Hastiludium",
    "name": "Protected Combo — Hasti variant", "video": "https://youtu.be/ItJLhNSCq6Y",
    "steps": [
        S("punishment", "E"),
        S("promptness", "SPACE"),
        S("purificatione", "SHIFT+LMB"),
        S("sacrum-ferit", "RMB", annot="1 hit"),
        S("hastiludium", "W+F"),
        S("terra-sancta", "S+RMB"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F/LMB"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("flow-divina-vult", "LMB", annot="Verdict cancel"),
    ],
    "notes": ["Feel free to cancel all hits of Sacrum Ferit with Guard for a shorter frontal "
              "guard. You'll get the crit buff regardless, but your add-ons won't apply."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-protected-casti", "mode": "pvp", "scale": "1v1", "protected": True,
    "family": "Protected", "core_variant": "Castigatio",
    "name": "Protected Combo — Casti variant", "video": "https://youtu.be/HcpZFngpPQY",
    "steps": [
        S("punishment", "E"),
        S("promptness", "SPACE"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F/LMB"),
        S("death-line-chase", "SHIFT+S"),
        S("sacrum-ferit", "RMB"),
        S("guard", "Q"),
        S("flow-lucem-fluxum", "Quick Slot"),
        S("purificatione", "SHIFT+LMB"),
        S("castigatio", "S+LMB"),
        S("terra-sancta", "Hold (after Castigatio)"),
        S("guard", "Q (S+Q)"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("flow-divina-vult", "LMB", annot="Verdict cancel"),
    ],
    "notes": [], "sources": [PVP], "conflicts": [],
})

# --- Finishers (modular tails appended to combos ending in Blitz Stab [+ Divina Inpulsa]) ---
COMBOS.append({
    "id": "pvp-finisher-1", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Finisher", "core_variant": "Option 1 (reset)",
    "name": "Finisher 1 — Reset", "video": None,
    "steps": [
        S("divine-power", "SHIFT+F"),
        S("celestial-spear", "S+E"),
        S("divine-judgment-of-light", "LMB"),
    ],
    "notes": ["Go-to if you're trying to reset; good damage (unprotected / possible reset).",
              "Append to any combo ending in Blitz Stab [+ Divina Inpulsa]. The target gets up "
              "during the finisher unless you land a reset."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-finisher-2", "mode": "pvp", "scale": "1v1", "protected": False,
    "family": "Finisher", "core_variant": "Option 2 (highest damage)",
    "name": "Finisher 2 — Highest damage", "video": None,
    "steps": [
        S("shield-chase", "SHIFT+A/D"),
        S("gladius-gloriae", "F"),
        S("celestial-spear", "S+E"),
        S("divine-judgment-of-light", "LMB"),
    ],
    "notes": ["Highest damage; gain distance to finish off your target (unprotected / no reset)."],
    "sources": [PVP], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-finisher-3", "mode": "pvp", "scale": "1v1", "protected": True,
    "family": "Finisher", "core_variant": "Option 3 (protected)",
    "name": "Finisher 3 — Protected", "video": None,
    "steps": [
        S("verdict-lancia-iustitiae", "SHIFT+RMB"),
        S("sanctitas-de-enslar", "F"),
        S("flow-divina-vult", "F"),
    ],
    "notes": ["Lower damage, somewhat vulnerable to grab but you can iframe them or go behind "
              "frontal guards with Sanctitas de Enslar (fully protected / no reset)."],
    "sources": [PVP], "conflicts": [],
})

# --- Large-Scale (sheet; the Discord defers large-scale to the spreadsheet) ---
COMBOS.append({
    "id": "pvp-ls-bsr-engage", "mode": "pvp", "scale": "large-scale", "protected": False,
    "family": "Large-Scale", "core_variant": None,
    "name": "100% BSR Engage", "video": None,
    "steps": [
        S("divina-impulsa", "SHIFT+Q", "AP BUFF"),
        S("sacrum-ferit", "RMB", "CRIT BUFF"),
        S("hastiludium", "W+F", "ENGAGE"),
        S("wave-of-light", "S+F (Q cancel)", "VACUUM"),
        S("sanctitas-de-enslar", "F", "100% BSR", annot="100% Black Spirit Rage / full-rage cast"),
        S("flow-divina-vult", "F", "DAMAGE"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB", "DAMAGE",
          annot="Full-cast Shift+RMB is more damage but locks you in Super Armor"),
        S("flow-divina-vult", "LMB", "DAMAGE", opt=True, annot="Verdict cancel"),
    ],
    "notes": ["Large-scale engage built around a 100% BSR Sanctitas de Enslar.",
              "Heal rotation: SA Heal (Breath of Elion, Shift+E) · Puri Heal (Purificatione, "
              "Shift+LMB) · Rabam Heal (Celestial Smite/Cry, Shift+X)."],
    "sources": [SHEET], "conflicts": [],
})

COMBOS.append({
    "id": "pvp-ls-rotation", "mode": "pvp", "scale": "large-scale", "protected": False,
    "family": "Large-Scale", "core_variant": None,
    "name": "Large-Scale Damage Rotation", "video": None,
    "steps": [
        S("divina-impulsa", "SHIFT+Q", "AP BUFF"),
        S("sacrum-ferit", "RMB", "CRIT BUFF"),
        S("hastiludium", "W+F", "ENGAGE"),
        S("castigatio", "S+LMB", "DAMAGE"),
        S("terra-sancta", "S+RMB", "DAMAGE"),
        S("sanctitas-de-enslar", "F", "DAMAGE"),
        S("flow-divina-vult", "F", "DAMAGE"),
        S("verdict-lancia-iustitiae", "SHIFT+RMB", "DAMAGE"),
        S("flow-divina-vult", "LMB", "DAMAGE", opt=True, annot="Verdict cancel"),
    ],
    "notes": ["The core-only form drops Castigatio (step 4)."],
    "sources": [SHEET], "conflicts": [],
})


def main():
    ids = {s["id"] for s in json.loads(SKILLS.read_text(encoding="utf-8"))["skills"]}
    problems = []
    seen = set()
    for c in COMBOS:
        if c["id"] in seen:
            problems.append(f"duplicate combo id {c['id']}")
        seen.add(c["id"])
        for i, st in enumerate(c["steps"]):
            sk = st.get("skill")
            if sk and sk not in ids:
                problems.append(f"{c['id']}[{i}]: unknown skill {sk}")
    if problems:
        print("COMBO PROBLEMS:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        sys.exit(1)

    out = {
        "meta": {
            "count": len(COMBOS),
            "category_enum": sorted(set(CAT_NORM.values())),
            "note": "One combo per combo. PvE combos merge the sheet (categories + inputs, "
                    "skill identities confirmed by the icon phash bridge) with the Discord "
                    "(skill names + usage); the sheet wins on conflicts. Hit-count tokens are "
                    "step annotations, not steps. PvP families are from the Discord (Sarron); "
                    "the sheet supplies the GRAB / Knockdown 1v1 templates and Large-Scale.",
        },
        "combos": COMBOS,
    }
    OUT.write_text(json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    pve = sum(1 for c in COMBOS if c["mode"] == "pve")
    pvp = sum(1 for c in COMBOS if c["mode"] == "pvp")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(COMBOS)} combos ({pve} PvE, {pvp} PvP).")


if __name__ == "__main__":
    main()
