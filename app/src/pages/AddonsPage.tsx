import { PageHeader, Section, Callout } from "../components/Section";
import SourceImage from "../components/SourceImage";

export default function AddonsPage() {
  return (
    <>
      <PageHeader title="Add-ons">
        Add-on sets are shown as the source screenshots only — never transcribed (error-prone, and
        the guide itself states add-ons are preference-based).
      </PageHeader>

      <Callout tag="PREFERENCE">
        These are one author's recommendations, not canonical truth. Change them to fit your playstyle.
      </Callout>

      <Section id="pvp" title="PvP — Sarron's add-ons" desc="Uncapped + Capped">
        <p className="note">
          Breakdown (labels from the sheet, not transcribed onto the image): Combo −20 DP / −20 Eva ·
          Engage uptime · Reposition uptime · SA trade / large-scale dmg · Crit + Down modifiers ·
          Combo Attack Speed + Crit Rate.
        </p>
        <SourceImage path="addons/sarron-pvp.png" alt="Sarron's PvP add-on set" />
      </Section>

      <Section id="pve" title="PvE — RoNNiE's add-ons" desc="One of, or THE best PvE Valk on EU">
        <p className="note">
          Breakdown: Intuitive DP-debuff stacking (2nd add-on is spot-dependent) · Highest-priority
          DPS-skill add-ons · Most-important opener-skill add-ons · Spammable handy add-ons.
        </p>
        <SourceImage path="addons/ronnie-pve.png" alt="RoNNiE's PvE add-on set" />
      </Section>
    </>
  );
}
