# Skill Roster — candidate Registry (fill `bdocodex_id` + `icon`)

Consolidated from `docs/discord-awakening-pve.md`, `docs/discord-awakening-pvp.md`, and the
spreadsheet's DPS chart + add-on screenshots. This is the **input to Phase 1**: every skill the
awakening playstyle references, with its canonical name, every shortcode alias seen (including
the source's typos), `kind`, where it's referenced, and Discord metadata. The two blank columns
(`bdocodex_id`, `icon`) are what Phase 1 fills from BDO Codex.

**Rules:**
- `id` is the proposed canonical kebab-case Registry id.
- **Shortcode aliases include the source's misspellings** — fold ALL of them into the
  shortcode→id alias table so combos resolve. Known typos flagged ⚠.
- `kind`: `awakening` | `pre-awakening` | `rabam` | `quick-slot` | `locked-only`.
  Per scope (ADR 0003 / CONTEXT), the Registry pulls Codex data for everything that **appears in
  a combo/catch/finisher**. `locked-only` skills appear *only* in the Locked-Skills reference
  list and need no Codex pull unless also referenced elsewhere (some are — flagged).
- ⚠ = needs human/Codex verification.

## NOT skills — do not create Registry entries for these

Discord shortcodes that are **modifiers or emojis**, not skills:
- `:3hits:` `:1hit:` `:ALLhits:` — hit-count modifiers on the *preceding* skill (almost always
  `:SacrumFerit:`), i.e. how many hits to land. Model as a step annotation, NOT a step.
- `:Down:` `:cry:` — decorative Discord emojis in prose.
- `:sidestep:` — the side-step dodge (input `A/D+RMB`); a movement action, likely not a distinct
  Codex skill. ⚠ Treat as an input/annotation unless Codex has a matching skill.

## Awakening skills

| Canonical name | id | shortcode aliases | DPS-chart name(s) | add-on label | referenced in | importance | usage (Discord) | bdocodex_id | icon |
|---|---|---|---|---|---|---|---|---|---|
| Sacrum Ferit | `sacrum-ferit` | `:SacrumFerit:` | Sacrum III, Sacrum I / II, Sacrum 3 hits | "Sacrum Felt I" ⚠ | PvE+PvP combos (crit prebuff) | 10 | Crit buff, Frontal DMG; 5s 80% crit, 5s cd | | |
| Flow: Lucem Fluxum | `flow-lucem-fluxum` | `:FlowLucemFluxum:` | Lucem Fluxum | | PvE+PvP combos | 2 | Filler; only after 3rd Sacrum hit or off hotbar | | |
| Purificatione | `purificatione` | `:Purificatione:` | Purificatione, Purificatione cancel | | PvE+PvP combos | 9 | Debuff (10s DP, 6s cd), Heal, Aggro; cast w/ Promptness cancel | | |
| Castigatio | `castigatio` | `:Castigatio:` | Casti, Casti cancel | | PvE+PvP combos (CORE) | 9 | Main DPS tool, very low cd | | |
| Hastiludium | `hastiludium` | `:Hastiludium:`, ⚠`Hastludium` (sheet add-on "Hastludium I") | Hasti, Hasti cancel | "Hastludium I" ⚠ | PvE+PvP combos (CORE) | 4 | Movement, Filler; after BlitzStab | | |
| Divina Impulsa | `divina-impulsa` | `:DivinaInpulsa:` ⚠(source spells "Inpulsa") | Divina Impulsa I/II/full | | PvE+PvP combos | 6 | Frontal DMG; after stab skills or Promptness | | |
| Verdict: Lancia Iustitiae | `verdict-lancia-iustitiae` | `:VerdictLanciaIustitiae:` | Verdict I/II/full cast, Verdict Vult cancel | | PvE+PvP combos | 10 | AOE DMG; cancel w/ Flow Divina Vult or Sanctitas | | |
| Sanctitas de Enslar | `sanctitas-de-enslar` | `:SanctitasdeEnslar:`, `:PrimeSanctitasDeEnslar:` | Sanctitas de Enslar, ...Vult cancel, ...BSR | "Sanctitas de Enslar" | PvE+PvP combos (CORE) | 10 | Pre-buff (10s AP, 9s cd), Movement jump | | |
| Flow: Divina Vult | `flow-divina-vult` | `:FlowDivinaVult:` | Divina Vult | "Divine Vault" ⚠(likely this) | PvE+PvP combos | 10 | Cancel to Sanctitas, AOE DMG, Eva debuff; LMB after Sanctitas | | |
| Blitz Stab | `blitz-stab` | `:BlitzStab:` | Blitz Stab | | PvE+PvP combos | 7 | Frontal DMG; hit something to avoid 2nd cast | | |
| Promptness | `promptness` | `:Promptness:`, ⚠`:Promptess:` (DPS chart "Promptess") | Promptess ⚠ | "Promptness" | PvE+PvP combos | 8 | Frontal DMG, Movement; Space after any combat action | | |
| Terra Sancta | `terra-sancta` | `:TerraSancta:` | Terra Sancta | "Terra Sancta" | PvE+PvP combos | 5 | Frontal DMG, long cd; after Castigatio or Q block | | |
| Wave of Light | `wave-of-light` | `:WaveOfLight:` | Wave of Light cancel | | PvE DSR p2, PvP catch | 1 | Vacuum, worse DP debuff; situational | | |
| Heaven's Echo | `heavens-echo` | `:HeavensEcho:` | | | pre-buff (BSR) | 10 | Pre-buff (1min DP+accuracy); Space during Q block w/ Lancia | | |
| Death Line Chase | `death-line-chase` | `:DeathLineChase:` | | | PvP protected combos, swaps | – | Movement; backward twice → pre-awak. Ebuff DLC trick | | |
| Guard (Forward Guard) | `guard` | `:Guard:` | | | PvP protected combos (S+Q / Q block) | – | FG block stance; the protected-combo enabler | | |

## Pre-awakening skills (referenced in awakening combos → in Registry)

| Canonical name | id | shortcode aliases | DPS / refs | importance | usage | bdocodex_id | icon |
|---|---|---|---|---|---|---|---|
| Gladius Gloriae | `gladius-gloriae` | `:GladiusGloriae:` | "Gladius (magnus) cancel"; PvP Double-KD, finishers; Tricks cancel | 7 | Frontal DMG, long cd; after Shield Chase | | |
| Severing Light | `severing-light` | `:SeveringLight:` | "Severing Light"; PvE Best DPS, PvP dmg variant | 3 | Filler; after Gladius Gloriae | | |
| Celestial Spear | `celestial-spear` | `:CelestialSpear:` | PvE+PvP combos, catches, finishers, swaps | 7 | Ranged DMG, Crit buff, Aggro | | |
| Counter | `counter` | `:Counter:` | "Counter + S.Throw cancel"; PvP Counter combo, catch (S+LMB) | 4 | Catch / cancel | | |
| Just Counter | `just-counter` | `:JustCounter:` | PvP catch (W+LMB, from Guard) | – | Catch (Guard only, else hotbar) | | |
| Shield Throw | `shield-throw` | `:ShieldThrow:` | "Counter + S.Throw cancel"; Counter+ShieldThrow+CelestialSpear cancel | – | Cancel-chain skill | | |
| Shield Chase | `shield-chase` | `:ShieldChase:` | PvE Best DPS, PvP finishers, swaps (Shift+A/D) | – | Engage/movement | | |
| Sharp Light | `sharp-light` | `:SharpLight:` | PvP Re-CC (Shift+LMB) | – | Re-CC (pre-awak) | | |
| Punishment | `punishment` | `:Punishment:` | PvP grab catch (E); locked-list (marni note) | – | Catch (grab); works in awakening | | |
| Divine Power | `divine-power` | `:DivinePower:` | PvP down-smash (Shift+F), finishers; locked-list | – | Down-smash / finisher dmg | | |
| Flying Kick | `flying-kick` | `:FlyingKick:` | PvP BlitzStab-variant dmg note | – | Extra-dmg filler | | |

## Rabam skills (referenced → in Registry)

| Canonical name | id | shortcode | DPS / refs | bdocodex_id | icon |
|---|---|---|---|---|---|
| Celestial Smite | `celestial-smite` | `:CelestialSmite:` | "Celestial Smite", "Celestial Smite + abs. spear"; swaps (Shift+X) | | |
| Divine Descent | `divine-descent` | `:DivineDescent:` | swaps (Shift+Z) | | |
| Divine Judgment of Light | `divine-judgment-of-light` | `:DivineJudgmentofLight:` | "D. Judgement of Light I cancel", "...full"; PvP down-smash & finishers (S+E→LMB) | | |
| Divine Slam | `divine-slam` | `:DivineSlam:` | PvP down-smash fishing (Shift+Z) ⚠ vs Divine Descent same input — verify | | |

## Quick-slot skills (reference list; Codex pull optional)

| Name | id | shortcode |
|---|---|---|
| Noble Spirit | `noble-spirit` | `:NobleSpirit:` |
| Shining Dash | `shining-dash` | `:ShiningDash:` |
| Elion's Blessing | `elions-blessing` | `:ElionsBlessing:` |

## Locked-only skills (Locked-Skills reference page; NO Codex pull unless also referenced above)

`:ForwardSlash:` Forward Slash · `:ChargingSlash:` Charging Slash · `:GlaringSlash:` Glaring
Slash · `:SwordofJudgment:` Sword of Judgment · `:FlurryofKicks:` Flurry of Kicks ·
`:FlowDoubleFlyingKick:` Flow: Double Flying Kick · `:ShieldStrike:` Shield Strike ·
`:ShieldCounter:` Shield Counter · `:ShieldPush:` Shield Push · `:SkywardStrike:` Skyward Strike
· `:Evasion:` Evasion · `:Vindicta:` Vindicta.
(Note: `:Punishment:`, `:DivinePower:`, `:FlowLucemFluxum:` also appear in the locked list but ARE
referenced in combos → they live in the sections above, not here.)

## Open verification items for Phase 1

1. ⚠ Add-on screenshot labels "Sacrum Felt I" / "Hastludium I" / "Divine Vault" appear to be OCR/
   spelling variants of Sacrum Ferit / Hastiludium / Flow Divina Vult — confirm against Codex.
2. ⚠ `Divine Slam` (Shift+Z) vs `Divine Descent` (Shift+Z) share an input — confirm whether these
   are the same skill under two names or two skills.
3. ⚠ `:PrimeSanctitasDeEnslar:` is the Prime-rank alias of Sanctitas de Enslar — confirm one id.
4. Confirm `Guard` and `sidestep` have (or don't have) distinct Codex skill entries vs being
   stance/dodge inputs.
5. The DPS chart has combination/cancel rows ("Celestial Smite + abs. spear", "Verdict Vult
   cancel") — these are measurements, not new skills; map to the base skill id + keep the row label.
