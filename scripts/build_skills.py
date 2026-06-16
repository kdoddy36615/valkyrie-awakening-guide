#!/usr/bin/env python3
"""Build data/skills.json — the canonical Awakening Valkyrie Skill Registry.

Mirrors maegu's build_abilities.py shape. The curated REGISTRY below holds the
human decisions (id, kind, shortcodes incl. every Discord typo, inputs, Discord
metadata). It is merged with:
  - research/bdocodex/tooltips.json        (Codex name, description, cd, mp, effects)
  - research/bdocodex/protection_curated.json (graded protection per mode + notes)
  - research/bdocodex/roster_id_map.json   (roster id -> bdocodex id)
  - research/bridge/icon_bridge.json       (sheet-icon phash bridge; flag unmatched)

Skill identity and protection come from BDO Codex (ADR 0002); the sheet has none.
Run from repo root:  PYTHONIOENCODING=utf-8 python scripts/build_skills.py
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BDO = ROOT / "research" / "bdocodex"
BRIDGE = ROOT / "research" / "bridge"
OUT = ROOT / "data" / "skills.json"

PULL_DATE = "2026-06-15"
TOOLTIP_SOURCE = "BDO Codex"
CORE_SKILL = "castigatio"

# CC tokens we surface from Codex effect lines (PvE/PvP control effects).
CC_RE = re.compile(r"\b(Bound|Knockdown|Knockback|Stun|Stiffness|Floating|Grapple|Spin)\b")
# A CC effect line *applies* a CC when the type word leads the line ("Bound on hits"),
# as opposed to a protection line ("Super Armor on Grapple"). PvP excludes "(PvE only)" lines.
CC_WORDS = ("Bound", "Knockdown", "Knockback", "Stun", "Stiffness", "Floating", "Spin")
CC_LEAD_RE = re.compile(r"^(" + "|".join(CC_WORDS) + r")\b")
PVP_DMG_RE = re.compile(r"damage in PvP only", re.IGNORECASE)


def extract_cc(effects):
    """Return (cc_pve, cc_pvp): ordered unique CC type words. PvP drops PvE-only lines."""
    pve, pvp = [], []
    for e in effects:
        m = CC_LEAD_RE.match(e)
        if not m:
            continue
        w = m.group(1)
        if w not in pve:
            pve.append(w)
        if "PvE only" not in e and w not in pvp:
            pvp.append(w)
    return pve, pvp

# Sheet combo-icons that did NOT phash-match their Registry skill (ADR 0002 — the
# Codex icon is authoritative; this flag records the bridge could not confirm it).
SHEET_ICON_UNMATCHED = {"death-line-chase", "divine-judgment-of-light", "elions-blessing"}

# ---------------------------------------------------------------------------
# Curated registry — the human decisions. Codex supplies name/description/etc.
# importance / usage_tags / recommended_usage come from the Discord guides
# (docs/discord-awakening-pve.md, sources/skill-roster.md).
# ---------------------------------------------------------------------------
REGISTRY = [
    # ---- Awakening kit ----
    dict(id="sacrum-ferit", kind="awakening", inputs=["RMB", "A/D + RMB"],
         shortcodes=[":SacrumFerit:"], importance=10,
         usage_tags=["Crit buff", "Frontal DMG"],
         recommended_usage="5s 80% crit buff with 5s cd; utilize its cooldown to the maximum. "
                           "The crit prebuff opener for nearly every combo. Add-on label: \"Sacrum Felt I\"."),
    dict(id="flow-lucem-fluxum", kind="awakening", inputs=["Hold RMB after Sacrum Ferit", "Quick Slot"],
         shortcodes=[":FlowLucemFluxum:"], importance=2,
         usage_tags=["Filler", "Frontal DMG"],
         recommended_usage="Does close to no DMG. Can only be used after 3rd Sacrum Ferit hit or off hotbar. "
                           "Recommended to lock if you're new to the class."),
    dict(id="purificatione", kind="awakening", inputs=["SHIFT + LMB"],
         shortcodes=[":Purificatione:"], importance=9,
         usage_tags=["Debuff", "Frontal DMG", "Heal", "Aggro"],
         recommended_usage="10s All-DP debuff on 6s cd. Cast only with a Promptness cancel."),
    dict(id="castigatio", kind="awakening", inputs=["S + LMB"],
         shortcodes=[":Castigatio:"], importance=9,
         usage_tags=["Frontal DMG", "Core"],
         recommended_usage="Main DPS tool, very low cooldown. The core skill of the kit."),
    dict(id="hastiludium", kind="awakening", inputs=["W + F"],
         shortcodes=[":Hastiludium:", ":Hastludium:", "Hastludium"], importance=4,
         usage_tags=["Movement", "Filler", "Frontal DMG", "Core"],
         recommended_usage="Use to travel larger distances, or cast only after Blitz Stab. "
                           "Add-on label: \"Hastludium I\"."),
    dict(id="divina-impulsa", kind="awakening", inputs=["SHIFT + Q"],
         shortcodes=[":DivinaInpulsa:", "Inpulsa", "Divina Impulsa"], importance=6,
         usage_tags=["Frontal DMG"],
         recommended_usage="Fairly low cd. Cast only after stab skills (Blitz Stab, Hastiludium, Sacrum Ferit) "
                           "or Promptness. Codex spells it \"Divina Inpulsa\"; roster id stays divina-impulsa."),
    dict(id="verdict-lancia-iustitiae", kind="awakening", inputs=["SHIFT + RMB"],
         shortcodes=[":VerdictLanciaIustitiae:"], importance=10,
         usage_tags=["AOE DMG"],
         recommended_usage="Long animation heavy hitter with decent AOE. Cancel with Flow: Divina Vult (LMB) "
                           "or Sanctitas de Enslar (F). Want DPS? Don't cancel. Want freedom of action? Cancel."),
    dict(id="sanctitas-de-enslar", kind="awakening", inputs=["F"],
         shortcodes=[":SanctitasdeEnslar:", ":PrimeSanctitasDeEnslar:", "PrimeSanctitasDeEnslar"], importance=10,
         usage_tags=["Pre-buff", "Movement", "Core"],
         recommended_usage="10s Melee AP buff on 9s cooldown, medium-range jump. Prime alias resolves here."),
    dict(id="flow-divina-vult", kind="awakening", inputs=["LMB or F after Sanctitas de Enslar"],
         shortcodes=[":FlowDivinaVult:", "Divine Vault", "Divina Vult"], importance=10,
         usage_tags=["Cancel", "AOE DMG", "Eva debuff"],
         recommended_usage="LMB always right after Sanctitas de Enslar; also LMB during Verdict to cancel it. "
                           "Add-on label: \"Divine Vault\"."),
    dict(id="blitz-stab", kind="awakening", inputs=["W + RMB"],
         shortcodes=[":BlitzStab:"], importance=7,
         usage_tags=["Frontal DMG"],
         recommended_usage="Just hit something to avoid the 2nd cast."),
    dict(id="promptness", kind="awakening", inputs=["SPACE"],
         shortcodes=[":Promptness:", ":Promptess:", "Promptess"], importance=8,
         usage_tags=["Frontal DMG", "Movement"],
         recommended_usage="Low cooldown DPS tool. SPACE after any combat action. DPS chart typo: \"Promptess\"."),
    dict(id="terra-sancta", kind="awakening", inputs=["S + RMB"],
         shortcodes=[":TerraSancta:"], importance=5,
         usage_tags=["Frontal DMG"],
         recommended_usage="Long cooldown, moderate DMG. Cast only after Castigatio, or from Q block (worse)."),
    dict(id="wave-of-light", kind="awakening", inputs=["S + F"],
         shortcodes=[":WaveOfLight:"], importance=1,
         usage_tags=["Vacuum", "Debuff"],
         recommended_usage="Vacuum, worse DP debuff. Situational. Cancel with Q block or Death Line Chase backwards."),
    dict(id="heavens-echo", kind="awakening", inputs=["SHIFT + Q", "SPACE during Q block with lancia"],
         shortcodes=[":HeavensEcho:"], importance=10,
         usage_tags=["Pre-buff"],
         recommended_usage="1 min DP and accuracy buff. SPACE during a Q block with your Lancia."),
    dict(id="death-line-chase", kind="awakening", inputs=["SHIFT + W", "SHIFT + S"],
         shortcodes=[":DeathLineChase:"], importance=None,
         usage_tags=["Movement"],
         recommended_usage="Movement; backward twice drops you into pre-awakening. Ebuff DLC: bind WW and use "
                           "Death Line Chase during your e-buff instead of the running animation."),
    dict(id="guard", kind="awakening", inputs=["Q"],
         shortcodes=[":Guard:"], importance=None,
         usage_tags=["Frontal Guard", "Stance"],
         recommended_usage="The Forward Guard block stance — the enabler for every Protected combo."),

    # ---- Pre-awakening skills that appear in awakening combos ----
    dict(id="gladius-gloriae", kind="pre-awakening", inputs=["F"],
         shortcodes=[":GladiusGloriae:"], importance=7,
         usage_tags=["Frontal DMG"],
         recommended_usage="Long cooldown, decent DMG. Use after Shield Chase."),
    dict(id="severing-light", kind="pre-awakening", inputs=["LMB + RMB"],
         shortcodes=[":SeveringLight:"], importance=3,
         usage_tags=["Filler", "Frontal DMG"],
         recommended_usage="Filler. Use after Gladius Gloriae."),
    dict(id="celestial-spear", kind="pre-awakening", inputs=["S + E"],
         shortcodes=[":CelestialSpear:"], importance=7,
         usage_tags=["Ranged DMG", "Crit buff", "Aggro"],
         recommended_usage="Ranged DMG, crit buff and aggro tool. Gives the crit-rate buff for nearly a whole combo."),
    dict(id="counter", kind="pre-awakening", inputs=["S + LMB"],
         shortcodes=[":Counter:"], importance=4,
         usage_tags=["Catch", "Cancel"],
         recommended_usage="Counter after Shield Chase into Shield Throw into Celestial Spear into Shield Throw — "
                           "a cancel chain worth learning."),
    dict(id="just-counter", kind="pre-awakening", inputs=["W + LMB during Guard"],
         shortcodes=[":JustCounter:"], importance=None,
         usage_tags=["Catch"],
         recommended_usage="Catch from Guard only, hotbar otherwise."),
    dict(id="shield-throw", kind="pre-awakening", inputs=["S + Q"],
         shortcodes=[":ShieldThrow:"], importance=None,
         usage_tags=["Cancel-chain"],
         recommended_usage="Part of the Counter / Shield Throw / Celestial Spear cancel chain."),
    dict(id="shield-chase", kind="pre-awakening", inputs=["Direction + SHIFT", "SHIFT + A/D"],
         shortcodes=[":ShieldChase:"], importance=None,
         usage_tags=["Engage", "Movement"],
         recommended_usage="Engage / movement. Swaps to pre-awakening (Shift+A/D)."),
    dict(id="sharp-light", kind="pre-awakening", inputs=["SHIFT + LMB"],
         shortcodes=[":SharpLight:"], importance=None,
         usage_tags=["Re-CC"],
         recommended_usage="Pre-awakening re-CC."),
    dict(id="punishment", kind="pre-awakening", inputs=["E"],
         shortcodes=[":Punishment:"], importance=None,
         usage_tags=["Catch", "Grab"],
         recommended_usage="Grab catch; works in awakening. (Lock it if you're a Marni-only grinder.)"),
    dict(id="divine-power", kind="pre-awakening", inputs=["SHIFT + F"],
         shortcodes=[":DivinePower:"], importance=None,
         usage_tags=["Down-smash", "Finisher DMG"],
         recommended_usage="Down-smash fishing and finisher damage."),
    dict(id="flying-kick", kind="pre-awakening", inputs=["S + F"],
         shortcodes=[":FlyingKick:"], importance=None,
         usage_tags=["Filler"],
         recommended_usage="Extra-damage filler in the Blitz Stab Double-KD variant."),

    # ---- Rabam skills ----
    dict(id="celestial-smite", kind="rabam", inputs=["SHIFT + X"],
         shortcodes=[":CelestialSmite:"], importance=None,
         usage_tags=["Rabam", "Crit buff", "DMG"],
         recommended_usage="Rabam. Pulls and bounds; pairs with Absolute: Celestial Spear for a strong cancel."),
    dict(id="divine-descent", kind="rabam", inputs=["SHIFT + Z"],
         shortcodes=[":DivineDescent:"], importance=None,
         usage_tags=["Rabam", "DP buff"],
         recommended_usage="Rabam. DP buff for self and allies. Shares the Shift+Z input with Divine Slam (loadout choice)."),
    dict(id="divine-judgment-of-light", kind="rabam", inputs=["LMB during Celestial Spear / Smite", "S + E -> LMB"],
         shortcodes=[":DivineJudgmentofLight:"], importance=None,
         usage_tags=["Rabam", "Down-smash", "Finisher DMG"],
         recommended_usage="Rabam finisher; needs Celestial Spear/Smite off cooldown."),
    dict(id="divine-slam", kind="rabam", inputs=["SHIFT + Z"],
         shortcodes=[":DivineSlam:"], importance=None,
         usage_tags=["Rabam", "Down-smash"],
         recommended_usage="Rabam down-smash fishing. Distinct from Divine Descent though both bind Shift+Z."),

    # ---- Quick-slot skills ----
    dict(id="noble-spirit", kind="quick-slot", inputs=["Quick Slot"],
         shortcodes=[":NobleSpirit:"], importance=None,
         usage_tags=["E-buff", "Quick-slot"],
         recommended_usage="Our E-buff; can only be cast from a quick slot."),
    dict(id="shining-dash", kind="quick-slot", inputs=["↑ + RMB", "Quick Slot"],
         shortcodes=[":ShiningDash:"], importance=None,
         usage_tags=["Movement", "Quick-slot"],
         recommended_usage="Useful for chasing people in duels; can only be cast from a quick slot."),
    dict(id="elions-blessing", kind="quick-slot", inputs=["Quick Slot"],
         shortcodes=[":ElionsBlessing:"], importance=None,
         usage_tags=["PA", "DP buff", "Quick-slot"],
         recommended_usage="Our PA (protected ability); can only be cast from a quick slot."),
]

# Locked-only skills (Reference "Skills to Lock"). id+name+icon only; no Codex tooltip.
# bdocodex_id from protection_curated.json["locked_only"]; icons resolved by fetch_icons.py.
LOCKED_ONLY = [
    dict(id="forward-slash", name="Forward Slash", shortcodes=[":ForwardSlash:"]),
    dict(id="charging-slash", name="Charging Slash", shortcodes=[":ChargingSlash:"]),
    dict(id="glaring-slash", name="Glaring Slash", shortcodes=[":GlaringSlash:"]),
    dict(id="sword-of-judgment", name="Sword of Judgment", shortcodes=[":SwordofJudgment:"]),
    dict(id="flurry-of-kicks", name="Flurry of Kicks", shortcodes=[":FlurryofKicks:"]),
    dict(id="flow-double-flying-kick", name="Flow: Double Flying Kick", shortcodes=[":FlowDoubleFlyingKick:"]),
    dict(id="shield-strike", name="Shield Strike", shortcodes=[":ShieldStrike:"]),
    dict(id="shield-counter", name="Shield Counter", shortcodes=[":ShieldCounter:"]),
    dict(id="shield-push", name="Shield Push", shortcodes=[":ShieldPush:"]),
    dict(id="skyward-strike", name="Skyward Strike", shortcodes=[":SkywardStrike:"]),
    dict(id="evasion", name="Evasion", shortcodes=[":Evasion:"]),
    dict(id="vindicta", name="Vindicta", shortcodes=[":Vindicta:"]),
]


def load(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    tooltips = load(BDO / "tooltips.json")
    roster_map = load(BDO / "roster_id_map.json")
    curated = load(BDO / "protection_curated.json")
    prot = curated["protection"]
    locked_ids = curated["locked_only"]

    skills = []
    problems = []

    for reg in REGISTRY:
        rid = reg["id"]
        bid = roster_map.get(rid)
        if bid is None:
            problems.append(f"{rid}: no bdocodex id in roster_id_map.json")
            continue
        tip = tooltips.get(str(bid))
        if tip is None:
            problems.append(f"{rid}: no tooltip for bdocodex id {bid}")
            continue

        effects = tip.get("effects", [])
        cc_lines = [e for e in effects if CC_RE.search(e)]
        cc_pve, cc_pvp = extract_cc(effects)
        pvp_damage = [e for e in effects if PVP_DMG_RE.search(e)]

        pmode = prot.get(rid)
        if pmode is None:
            problems.append(f"{rid}: no curated protection")
            continue
        pve, pvp, note = pmode

        skill = {
            "id": rid,
            "name": tip["name"],
            "kind": reg["kind"],
            "shortcodes": reg["shortcodes"],
            "inputs": reg["inputs"],
            "icon": rid,
            "importance": reg["importance"],
            "usage_tags": reg["usage_tags"],
            "recommended_usage": reg["recommended_usage"],
            "protection": {
                "pve": pve,
                "pvp": pvp,
                "tooltip_lines": tip.get("protection_lines", []),
                "notes": note,
                "source": TOOLTIP_SOURCE,
                "source_url": tip.get("url"),
                "pulled": PULL_DATE,
            },
            "description": tip.get("description"),
            "cooldown": tip.get("cooldown"),
            "mp_cost": tip.get("mp_cost"),
            "required_level": tip.get("required_level"),
            "effects": effects,
            "cc_lines": cc_lines,
            "cc": cc_pve,
            "cc_pvp": cc_pvp,
            "pvp_damage": pvp_damage,
            "bdocodex_id": bid,
            "sheet_icon_matched": rid not in SHEET_ICON_UNMATCHED,
        }
        skills.append(skill)

    # Locked-only: minimal entries for the Reference page.
    for lk in LOCKED_ONLY:
        rid = lk["id"]
        bid = locked_ids.get(rid)
        if bid is None:
            problems.append(f"{rid}: locked-only with no bdocodex id")
        skills.append({
            "id": rid,
            "name": lk["name"],
            "kind": "locked-only",
            "shortcodes": lk["shortcodes"],
            "inputs": [],
            "icon": rid,
            "importance": None,
            "usage_tags": ["Locked"],
            "recommended_usage": "Recommended to lock for newer players (some are preference after the basics).",
            "protection": None,
            "description": None,
            "cooldown": None,
            "mp_cost": None,
            "required_level": None,
            "effects": [],
            "cc_lines": [],
            "cc": [],
            "cc_pvp": [],
            "pvp_damage": [],
            "bdocodex_id": bid,
            "sheet_icon_matched": True,
        })

    if problems:
        print("BUILD PROBLEMS:", file=sys.stderr)
        for p in problems:
            print("  -", p, file=sys.stderr)
        sys.exit(1)

    out = {
        "meta": {
            "pull_date": PULL_DATE,
            "tooltip_source": TOOLTIP_SOURCE,
            "core_skill": CORE_SKILL,
            "protection_enum": ["iframe", "super_armor", "frontal_guard", "none"],
            "count": len(skills),
            "note": "Skill identity + protection from BDO Codex (ADR 0002). Sheet has neither. "
                    "Pre-awakening skills included only when they appear in awakening combos.",
        },
        "skills": skills,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {OUT.relative_to(ROOT)} — {len(skills)} skills "
          f"({sum(1 for s in skills if s['kind']=='awakening')} awakening, "
          f"{sum(1 for s in skills if s['kind']=='pre-awakening')} pre-awakening, "
          f"{sum(1 for s in skills if s['kind']=='rabam')} rabam, "
          f"{sum(1 for s in skills if s['kind']=='quick-slot')} quick-slot, "
          f"{sum(1 for s in skills if s['kind']=='locked-only')} locked-only).")


if __name__ == "__main__":
    main()
