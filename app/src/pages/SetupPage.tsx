import { setupFile, maybeSkill } from "../data";
import type { SetupEntry, Mode } from "../data/types";
import { PageHeader, Section, Callout } from "../components/Section";
import AbilityIcon from "../components/AbilityIcon";
import SourceImage from "../components/SourceImage";

function EntryItem({ e }: { e: SetupEntry }) {
  const s = maybeSkill(e.skill);
  const name = s?.name ?? e.name ?? e.skill ?? "—";
  return (
    <div className="hotbar-slot">
      <div className="slot-name">
        {s && <AbilityIcon id={s.id} size="row" />}
        {name}
      </div>
      {e.tier && <span className="badge optional" style={{ marginTop: 2 }}>{e.tier}</span>}
      {e.note && <p className="dim" style={{ margin: "4px 0 0" }}>{e.note}</p>}
    </div>
  );
}

function EntryRow({ items }: { items: SetupEntry[] }) {
  return <div className="hotbar-row">{items.map((e, i) => <EntryItem key={i} e={e} />)}</div>;
}

const TIERS = ["Required", "Important", "Quality of Life", "Additional"];

export default function SetupPage({ mode }: { mode: Mode }) {
  const m = setupFile.modes[mode];
  const label = mode === "pve" ? "PvE" : "PvP";

  return (
    <>
      <PageHeader title={`Setup — ${label}`}>
        Loadout for {label}: core skill, Rabam (skill enhancement) picks, the add-on set, quick-slots,
        and which skills to lock. Sourced from {mode === "pve" ? "RoNNiE's PvE guide" : "Sarron's PvP guide"} and the spreadsheet.
      </PageHeader>

      <Section id="core" title="Core Skill" count={m.core.length} desc={m.core_note}>
        <EntryRow items={m.core} />
      </Section>

      <Section id="rabams" title="Rabam (Skill Enhancement)" count={m.rabams.length} desc={m.rabam_note}>
        <EntryRow items={m.rabams} />
      </Section>

      {m.downsmash && (
        <Section id="downsmash" title="Down-Smash Fishing" count={m.downsmash.length} desc={m.downsmash_note}>
          <EntryRow items={m.downsmash} />
        </Section>
      )}

      <Section id="addon" title="Add-ons" desc={m.addon.caption}>
        <Callout tag="PREFERENCE">
          Add-ons are preference-based — one author's recommendation, shown as the source screenshot
          (never transcribed). Breakdown: {m.addon.breakdown.join(" · ")}.
        </Callout>
        <SourceImage path={m.addon.image} alt={m.addon.caption} />
      </Section>

      <Section id="quickslot" title="Quick-slot Skills" count={setupFile.quickslot.length}
        desc="General (not mode-specific in the source)">
        {TIERS.map((tier) => {
          const items = setupFile.quickslot.filter((q) => q.tier === tier);
          if (!items.length) return null;
          return (
            <div key={tier}>
              <div className="micro">{tier}</div>
              <EntryRow items={items} />
            </div>
          );
        })}
      </Section>

      {mode === "pve" ? (
        <Section id="locked" title="Skills to Lock" count={m.locked.length} desc={m.locked_note}>
          <EntryRow items={m.locked} />
        </Section>
      ) : (
        <Section id="locked" title="Locking" desc={m.locked_note}>
          <Callout tag="NOTE">{m.locked_note}</Callout>
          <div className="micro">PvP unlocks these (PvE locks them)</div>
          <EntryRow items={m.pvp_unlocks ?? []} />
        </Section>
      )}
    </>
  );
}
