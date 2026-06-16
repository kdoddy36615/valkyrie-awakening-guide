import { combos } from "../data";
import type { Combo, Mode } from "../data/types";
import { PageHeader, Section, Callout } from "../components/Section";
import ComboStrip from "../components/ComboStrip";

function ComboCard({ combo, mode }: { combo: Combo; mode: Mode }) {
  const meta: string[] = [];
  if (combo.core_variant) meta.push(combo.core_variant);
  if (combo.scale) meta.push(combo.scale === "1v1" ? "1v1" : "Large-Scale");
  meta.push(`${combo.steps.length} steps`);
  return (
    <div className="combo-card" id={combo.id}>
      <h3>
        {combo.name}
        {combo.protected && <span className="badge tier-top" style={{ marginLeft: 8 }}>PROTECTED</span>}
        {combo.conflicts.length > 0 && <span className="badge unknown" style={{ marginLeft: 6 }} title="Sources diverge — see below">CONFLICT</span>}
      </h3>
      <p className="combo-meta">{meta.join(" · ")}</p>
      <ComboStrip combo={combo} mode={mode} />
      {combo.conflicts.length > 0 && (
        <ul className="notes" style={{ marginTop: 8 }}>
          {combo.conflicts.map((c, i) => <li key={i} style={{ color: "var(--warn)" }}>⚠ {c}</li>)}
        </ul>
      )}
      <p className="prov">
        Sources: {combo.sources.map((s) => s.ref + (s.updated ? ` (${s.updated})` : "")).join(" · ")}
        {combo.video && <> · <a href={combo.video} target="_blank" rel="noreferrer">video ▶</a></>}
      </p>
    </div>
  );
}

function familyGroups(list: Combo[]): { family: string; items: Combo[] }[] {
  const order: string[] = [];
  const map = new Map<string, Combo[]>();
  for (const c of list) {
    if (!map.has(c.family)) { map.set(c.family, []); order.push(c.family); }
    map.get(c.family)!.push(c);
  }
  return order.map((f) => ({ family: f, items: map.get(f)! }));
}

export default function CombosPage() {
  const pve = combos.filter((c) => c.mode === "pve");
  const aos1v1 = combos.filter((c) => c.mode === "pvp" && c.scale === "1v1");
  const large = combos.filter((c) => c.mode === "pvp" && c.scale === "large-scale");

  return (
    <>
      <PageHeader title="Combos">
        Fixed taught sequences as in-game combo strips — one combo per combo, merged from the
        spreadsheet and Discord. Each step shows its input, category, and per-mode protection.
      </PageHeader>

      <Callout tag="AOS">
        PvP scope is AOS (capped 3v3). The guide has no AOS-specific combos, so AOS is drawn from
        both 1v1 (grab/CC/burst) and Large-Scale (protected SA/FG emphasis).
      </Callout>

      <Section id="pve" title="PvE" count={pve.length} desc="RoNNiE's rotations — not loopable">
        {pve.map((c) => <ComboCard key={c.id} combo={c} mode="pve" />)}
      </Section>

      <Section id="pvp-1v1" title="PvP — AOS 1v1" count={aos1v1.length} desc="Sarron's combo families">
        {familyGroups(aos1v1).map((g) => (
          <div key={g.family}>
            <div className="micro">{g.family}</div>
            {g.items.map((c) => <ComboCard key={c.id} combo={c} mode="pvp" />)}
          </div>
        ))}
      </Section>

      <Section id="pvp-large" title="PvP — Large-Scale" count={large.length} desc="From the spreadsheet">
        {large.map((c) => <ComboCard key={c.id} combo={c} mode="pvp" />)}
      </Section>
    </>
  );
}
