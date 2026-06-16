# Implementation Notes (distilled from maegu + sources)

Working reference so we don't re-read maegu. Captures the engineering skeleton to copy and
the key facts extracted from the valkyrie sources. See HANDOFF.md / CONTEXT.md / ADRs for decisions.

## Repo layout to build (mirror maegu)
```
package.json            (type:module; scripts: dev=vite, build="tsc --noEmit && vite build",
                         preview=vite preview, validate="python scripts/validate_data.py")
vite.config.ts          root:"app", publicDir:false, server.fs.allow:[".."], build.outDir:"../dist"
tsconfig.json           strict, jsx react-jsx, resolveJsonModule, include ["app/src"]
data/*.json             skills.json, combos.json, dps.json, tricks.json, theory.json
app/index.html          #root + module script /src/main.tsx
app/src/main.tsx        React 18 createRoot + <HashRouter><App/>
app/src/App.tsx         Routes + Sidebar shell
app/src/styles.css      dark-slate theme (copy maegu, swap accent to gold/light-blue)
app/src/data/{index.ts,types.ts}
app/src/toc.ts
app/src/pages/*.tsx
app/src/components/*.tsx
app/src/assets/icons/<id>.webp        (fetch_icons.py output)
app/src/assets/addons/*.png           (add-on screenshots)
scripts/extract_xlsx.py  fetch_icons.py  validate_data.py  build_skills.py  smoke.mjs
research/bdocodex/{raw/,icons/,parse_tooltips.py,tooltips.json}
sources/                 lossless extract from xlsx (text + images + skill-roster.md already exists)
```

### Deps (package.json)
- dependencies: react ^18.3.1, react-dom ^18.3.1, react-router-dom ^6.30.0
- devDependencies: @types/react ^18.3.18, @types/react-dom ^18.3.5, @vitejs/plugin-react ^4.3.4,
  puppeteer-core ^25.1.0, typescript ^5.7.3, vite ^6.2.0

## maegu engineering patterns to copy

### main.tsx
```tsx
import React from "react"; import ReactDOM from "react-dom/client";
import { HashRouter } from "react-router-dom"; import App from "./App"; import "./styles.css";
ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode><HashRouter><App/></HashRouter></React.StrictMode>);
```

### Routing
maegu uses `/:mode/:page` with a global PVE|PVP toggle. **Valkyrie is simpler**: no global mode
toggle needed — pages are Skills, Combos, Practice, Add-ons, Tricks, DPS, Reference, R1 AOS.
Use HashRouter, a Sidebar with NavLink list, and a route per page. Combos page internally
sections PvE / PvP-AOS-1v1 / PvP-Large-Scale.

### data/index.ts pattern
- `import skillsJson from "../../../data/skills.json"` etc., cast `as unknown as SkillsFile`.
- Build `skillById = new Map`, `skill(id)` throw-if-missing helper.
- Alias table: shortcode→id Map folding ALL aliases incl. typos.
- PROTECTION_LABEL / PROT_RANK{iframe:4,super_armor:3,frontal_guard:2,none:1} / PROT_SHORT
  {IFRAME,SA,FG,UNPROT}.
- DEV-only referential check via `import.meta.env.DEV`.

### AbilityIcon.tsx
```tsx
const icons = import.meta.glob("../assets/icons/*.webp",{eager:true,query:"?url",import:"default"}) as Record<string,string>;
export function iconUrl(id){ return icons[`../assets/icons/${id}.webp`]; }
// sizes sm(17px)/row(22px)/xl(58px); render <img class="ability-icon {size}">
```

### SourceImage.tsx
`import.meta.glob("../../../sources/**/*.png",...)` OR put add-on shots in app/src/assets and glob
those. Framed thumbnail (360px) + click-to-zoom lightbox, Esc closes. Data carries the path.

### badges.tsx — ProtMeter
4-dot meter (filled=PROT_RANK) + mono short label, colored by `--iframe/--sa/--fg/--none`.
PROT_COLOR map → CSS vars. CcBadges, Kbd, AbilityLink(icon+short_name → /skills#id).

### ComboStrip.tsx (the centerpiece)
Black panel; per step: input chip above, xl icon, ProtMeter, optional dps/cc/category caption.
choices → "OR" stacks. `optional` → "OPTIONAL" caption. notes <ul>. For valkyrie add a
category label caption per step (FLOATING/TRANSITION/CRIT BUFF/etc.) and protection badge per mode.

### DpsTable.tsx
Renders rows verbatim, `fmt` = toLocaleString maxFractionDigits. Never recompute.

### Section.tsx
`<Section id title count desc>`, `<PageHeader title>{sub}`, `<Callout tag warn>`.

### styles.css theme tokens (copy maegu, swap accents)
maegu vars: --bg#0d1014 --bg-raised#12161b --bg-hover#1a1f26 --border#222831 --border-strong#2e3640
--text#d3dae0 --text-dim#84909c --text-faint#59646f. Protection: --iframe#9d7bff --sa#e8b14e
--fg#4ec9b0 --none#e0697a. CC --cc#f0a8b8. Fonts IBM Plex Sans/Mono (Google Fonts link in index.html).
**Valkyrie accent change**: --accent gold `#e8c060`-ish + secondary light-blue `#8fд8e0`. Use gold
as primary accent, light-blue as secondary highlight. Keep protection palette unchanged.
Layout: `.app` grid 232px sidebar + 1fr main. All the component classes (.combo-strip, .strip-*,
.prot/.meter, .badge, .kbd, .sec/.sechead, .callout, .cards/.card, .dps-table, .thumb/.lightbox,
.hotbar-*, ledger .cols/.lrow/.lexp) — copy maegu styles.css wholesale, retint accent.

### scripts/build (maegu build_abilities.py shape)
A python REGISTRY list of dicts (curated ids/shortcodes/inputs/kind/protection enums) + merge with
parsed Codex tooltips.json (descriptions, protection_lines, cooldown, effects) → data/skills.json.
PULL_DATE constant, TOOLTIP_SOURCE="BDO Codex".

### research/bdocodex/parse_tooltips.py
Regex-parse `raw/skill-<ID>.html` (tip.php output). Extracts: name (`tag_skill_name`), name_kr,
description (`tag_skill-description`), input (`tag_control`), required_level, mp (`tag_required_mp`),
cooldown (`tag_cooldown`), effects (`<div id="description">` → lines), protection_lines =
lines matching /Invincible|Super Armor|Forward Guard/. Writes tooltips.json keyed by id.
Refresh: `curl "https://bdocodex.com/tip.php?id=skill--<ID>&l=us" -o raw/skill-<ID>.html`.

### fetch_icons.py
For each skill with tooltip: dest app/src/assets/icons/<id>.webp. Reuse if exists or in
research/bdocodex/icons/<sid>.webp. Else parse raw html for `<img src="(/items/..\.webp)" alt="icon" width="40"`,
download from https://bdocodex.com + path, sleep 0.3.

### validate_data.py
Load skills.json → IDS set. walk() combos/dps/tricks/theory recursively; any field in id_fields
({skill,skills,choices,...}) must resolve to a known id (null allowed for flagged unmatched).
exit 1 with messages on error; else print OK.

### smoke.mjs
puppeteer-core launching local chrome/edge; visit each hash route; fail on console errors / <200
chars; screenshot to .screenshots/.

## KEY SOURCE FACTS already extracted

### From xlsx "Important Info" sheet (text_dump rows ~93-135) — PROTECTION + CC CROSS-CHECK
The sheet DOES carry per-skill Protection + CC (awakening table, cols I-M rows 49-68). Use as
cross-check/fallback vs Codex. Awakening skills (Skill | CC | Protection | Input):
- Sacrum Ferit | Stiffness 1st hit, Floating 3rd hit (PvE) | Frontal Guard | RMB, A/D+RMB
- Flow: Lucem Fluxum | Knockdown | Frontal Guard | RMB after Sacrum Ferit, Quick Slot
- Purificatione | Stun (PvE) | Frontal Guard | SHIFT+LMB
- Castigatio | Bound | - (none) | S+LMB
- Hastiludium | Knockdown (PvE) | Super Armor | W+F
- Divina Inpulsa | Knockdown (PvE) | Frontal Guard | SHIFT+Q
- Verdict: Lancia Iustitiae | Knockdown (PvE) | Super Armor | SHIFT+RMB
- Sanctitas de Enslar | Stiffness on marked hits, Knockdown on last hits (PvE) | Iframe into SA | F
- Flow: Divina Vult | - | Super Armor | LMB or F
- Blitz Stab | Knockdown | - (none) | W+RMB
- Promptness | Stiffness (PvE) | Super Armor | SPACE
- Terra Sancta | Bound (PvE) | Super Armor | S+RMB
- Wave of Light | Bound | - (none) | S+F
- Death Line Chase | - | FG+SA | SHIFT+W/S
- Noble Spirit | - | FG+SA (while sprinting) | Quick Slot
- Vindicta | Knockback | FG+SA | LMB while on Guard
Pre-awak (cols C-F rows 50-89): Severing Light|Knockback|-|LMB+RMB; Divine Power|Bound(PvE)|Super Armor|SHIFT+F;
Celestial Spear|Bound|-|S+E; Gladius Gloriae|Knockdown|-|F; Punishment|Floating on Grapple|Super Armor on Grapple|E;
Counter|Floating, Bound on spin|-|S+LMB; Shield Throw|Stun|-|S+Q; Just Counter|Stiffness(PvE)|Frontal Guard|W+LMB while on Guard;
Sharp Light|Knockdown|-|SHIFT+LMB; Shield Chase|-|FG+SA|SHIFT+Direction; Flying Kick|Knockback|-|S+F.
Succession-prefixed entries are SUCCESSION (skip). Rabams from Important Info: Celestial Smite|Bound CC, crit+slow;
Divine Slam|Frontal Guard, down-smash chance; Divine Descent|Super Armor, DP buff; Divine Judgment of Light|atk/cast slow.
NOTE: protection enum maps: "Frontal Guard"/"FG"→frontal_guard, "Super Armor"/"SA"→super_armor,
"Iframe into SA"/"Partial Iframe"→iframe (graded top), "FG+SA"→super_armor (has SA, treat as full;
note FG too), "-"→none. Codex tooltip is authoritative per ADR; sheet is the cross-check.

### Buffs/Debuffs (Important Info K col) — useful for usage notes
Crit Hit Rate +80% 5s: Celestial Spear, Celestial Smite, Sacrum Ferit. Melee AP +32 10s: Sanctitas de Enslar,
Divina Inpulsa. AP +36: Shield Chase, Severing Light. DP -20 10s (All DP debuff): Purificatione, Wave of Light.
Eva -12 10s: Blitz Stab, Flow: Divina Vult, Gladius Gloriae. Move slow -15%: Verdict, Celestial Spear, Celestial Smite.
Atk/Cast slow -10%: Divine Judgment of Light, Divine Power. Guard: DP+30 20s. Heaven's Echo: +20 Accuracy 60s, nullify DR.

### DPS chart (xlsx sheet "Awakening PvE DPS chart") — LOCKED, copy verbatim
Header: A1="60%", cols = [skill-label, hit number, Damage, Total DMG, duration[s], DPS].
Provenance: H3="Made by @RonnieBDO", H6="Values are not frame exact", H7="But they are more or less accurate".
Rows (label | hits | damage | total | duration | dps) — map label→skill id (keep label):
Purificatione cancel|3.0|4295.0|12885|0.2|64425 → purificatione (cancel)
Wave of Light cancel|4.0|1245.0|4980|0.1|49800 → wave-of-light (cancel)
Divina Vult|2.0|7392.0|14784|0.4|36960 → flow-divina-vult
Gladius (magnus) cancel|3.0|7201.0|21603|0.6|36005 → gladius-gloriae (cancel)
Blitz Stab|4.0|6296.0|25184|0.8|31480 → blitz-stab
Casti cancel|3.0|6260.0|18780|0.6|31300 → castigatio (cancel)
D. Judgement of Light I cancel|2.0|5424.0|10848|0.4|27120 → divine-judgment-of-light (I cancel)
Sacrum III|2.0|5267.0|10534|0.4|26335 → sacrum-ferit (III)
Purificatione|3.0|4295.0|12885|0.5|25770 → purificatione
Terra Sancta|2.0|12593.0|25186|1.0|25186 → terra-sancta
Verdict Vult cancel|—|—|38714.0|1.6|24196.25 → verdict-lancia-iustitiae (vult cancel)
Sanctitas de Enslar Vult cancel|—|—|33504.0|1.4|23931.43 → sanctitas-de-enslar (vult cancel)
Verdict I|6.0|5882.0|35292|1.5|23528 → verdict-lancia-iustitiae (I)
Verdict full cast|—|—|55354.0|2.5|22141.6 → verdict-lancia-iustitiae (full)
Lucem Fluxum|2.0|5267.0|10534|0.5|21068 → flow-lucem-fluxum
Verdict II|2.0|10031.0|20062|1.0|20062 → verdict-lancia-iustitiae (II)
Promptess|2.0|2920.0|5840|0.3|19466.67 → promptness  (typo "Promptess")
Sanctitas de Enslar BSR|4.0|12909|51636|2.8|18441.43 → sanctitas-de-enslar (BSR)
Sacrum 3 hits|—|—|21068.0|1.2|17556.67 → sacrum-ferit (3 hits)
Celestial Smite + abs. spear|—|—|8622.0|0.5|17244 → celestial-smite (+ celestial-spear) combo measurement
Casti|3.0|6260.0|18780|1.1|17072.73 → castigatio
Sanctitas de Enslar|2.0|7800.0|18720|1.1|17018.18 → sanctitas-de-enslar
Severing Light|—|—|8169|0.5|16338 → severing-light
Divina Impulsa II|4.0|3868.0|15472|1.0|15472 → divina-impulsa (II)
Divine Judgement of Light full|4.0|5424.0|21696|1.6|13560 → divine-judgment-of-light (full)
Counter + S.Throw cancel|—|—|10644|0.8|13305 → counter (+ shield-throw) combo measurement
Sacrum I / II|1.0|5267.0|5267|0.4|13167.5 → sacrum-ferit (I/II)
Celestial Smite|2.0|3285.0|6570|0.5|13140 → celestial-smite
Divina Impulsa full|—|—|17406|1.5|11604 → divina-impulsa (full)
Hasti cancel|2.0|3037.0|6074|0.8|7592.5 → hastiludium (cancel)
Hasti|2.0|3037.0|6074|1.0|6074 → hastiludium
Divina Impulsa I|1.0|1934.0|1934|0.5|3868 → divina-impulsa (I)
(divina-impulsa id note: roster uses `divina-impulsa`; DPS chart spells "Divina Impulsa", Discord "Inpulsa".)

### Combo category labels + inputs from xlsx "Awakening (Combos, Add-ons)" sheet
This sheet gives PvE combos as category-label + input strips (icons are images). Discord supplies
skill identities. MERGE per HANDOFF Phase 2. The sheet's three PvE combos:
- BEST DPS COMBO (row 43-46): categories AP BUFF|EVA DEBUFF|DP DEBUFF|...|EVA DEBUFF|AP BUFF|CRIT BUFF|DP DEBUFF|EVA DEBUFF|CRIT BUFF|DP DEBUFF
  inputs row46: F|LMB/F|S+LMB|SPACE|SHIFT+LMB|SHIFT+RMB|W+RMB|SHIFT+Q|RMB|RMB(FLOW)|SPACE|SHIFT+LMB|S+LMB|S+RMB|SHIFT+DIRECTION|LMB+RMB|F|S+E|SPACE|SHIFT+LMB
  → matches Discord "Best DPS Combo" (Sanctitas>FlowDivinaVult>Castigatio>Promptness>Purificatione>Verdict>BlitzStab>DivinaInpulsa>SacrumFerit>LucemFluxum>Promptness>Purificatione>Castigatio>TerraSancta>ShieldChase>GladiusGloriae>SeveringLight>CelestialSpear>Promptness>Purificatione)
- GYFIN COMBO (row 48-51): inputs F|LMB/F|SPACE|SHIFT+LMB|S+LMB|SHIFT+RMB|W+RMB|W+F|SHIFT+Q|SPACE|SHIFT+LMB|S+LMB|RMB
  → Discord "Recommended Gyfin combo".
- DARKSEEKERS COMBO (DSR) rows 53-61, LOOP 1 + LOOP 2 → Discord "DSR combo" phase1/phase2.
PvP section (rows 12-23): GRAB combo + KNOCKDOWN(CORE ONLY) combo with category labels
(FLOATING|TRANSITION|CRIT BUFF|AP BUFF|RE'CC|DEBUFF|DAMAGE...) and per-step inputs; plus
"Large Scale combos" (100% BSR engage + heal rotation, rows 26-37) and Finishers (col O).
Category enum (verbatim seen): FLOATING, TRANSITION, CRIT BUFF, AP BUFF, RE'CC, DEBUFF, DAMAGE,
ENGAGE, VACUUM, EVA DEBUFF, DP DEBUFF, 100% BSR, KNOCKDOWN. Normalize to:
floating, transition, crit-buff, ap-buff, re-cc, debuff, eva-debuff, dp-debuff, damage, engage,
vacuum (+ keep category_raw).

### Add-on screenshots (xlsx) — images only, DO NOT transcribe
PvP "Sarron's add-ons" (sheet4 ~row 68-90) breakdown labels: Combo -20dp+-20eva / Engage uptime /
Reposition uptime / SA trade-largescale dmg / Crit+Down Modifiers / Combo Attk Speed+Crit Rate.
PvE "@RoNNiE add-ons" (~row 97-114) breakdown: Intuitive DP debuff stacking / Highest priority dps
add-ons / Most important opener skill addons / Spammable handy add-ons. Extract the add-on image
regions from xl/media via drawing4 anchors (sheet4) → app/src/assets/addons/. Flag which media is which.

### Tricks (xlsx "Awakening Tricks" sheet5) — has xlsx comments (comments1.xml)
Cancels w/ `➔` sequences: Verdict Cancel (SHIFT+RMB ➔ LMB / ➔ LMB➔Q / ➔ Q+A/D+LMB / ➔ F),
Enslar Cancels (F ➔ LMB➔Q / ➔ Q+A/D+LMB; S+E ➔ F; Shift+X ➔ F), Castigatio Cancel
(SHIFT+LMB ➔ S+LMB; LMB/F ➔ S+LMB), Vacuum Cancel (S+F ➔ Q / SHIFT+A/D / SHIFT+W/S / S+E / F),
Gladius Gloriae Cancel (many ➔ F), Terra Sancta Cancel (S+LMB hold ➔ -; S+RMB ➔ S+Q),
Divina Inpulsa Cancel (W+RMB/W+F/RMB/SPACE/A/D+LMB ➔ SHIFT+Q), Hastiludium Charge-Up Cancel
(SHIFT+W ➔ W+F), Celestial Smite Cancel (E➔SHIFT+X➔SPACE➔SHIFT+LMB), Shining Judgment of Light
Cancel (W+F ➔ SPACE). Transitions Pre-awake⇄Awake tables (with Protected? column). Macros:
Ebuff DLC (bind WW, use Death Line Chase during ebuff). BSR Macros = ASCII art (decorative, keep in
sources, render monospace or omit). Movement combos. "Skills to Lock" list (col Q).

## Open verification items (roster §Open) — resolutions
1. Add-on OCR labels "Sacrum Felt I"/"Hastludium I"/"Divine Vault" = Sacrum Ferit / Hastiludium /
   Flow Divina Vult. CONFIRMED by context (they're the add-on screenshot labels). Note in data.
2. Divine Slam (Shift+Z) vs Divine Descent (Shift+Z): Important Info lists BOTH as distinct skills
   (Divine Slam=Frontal Guard down-smash; Divine Descent=Super Armor DP buff). Two skills, same input
   (different loadout choices). Keep both ids.
3. PrimeSanctitasDeEnslar = Prime-rank alias of Sanctitas de Enslar → single id sanctitas-de-enslar,
   both shortcodes alias to it.
4. Guard = real stance skill (Important Info row J21 "Guard | DP+30 20s"; FG block stance). Keep id
   `guard`. sidestep = movement input, NOT a skill (roster says so) → annotation only.
5. DPS combination rows ("Celestial Smite + abs. spear", "Verdict Vult cancel") = measurements;
   map to base skill id + keep row label. Done in DPS map above.

## bdocodex IDs — TBD in Phase 1
Need to find skill ids for each Valkyrie awakening skill on bdocodex.com (Valkyrie class).
Flow: search bdocodex Valkyrie skill list, curl tip.php?id=skill--<ID>&l=us. If network blocked,
fall back to sheet "Important Info" protection/CC as the protection source and flag source as sheet.
</content>
