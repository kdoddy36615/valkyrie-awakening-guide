import referenceJson from "../../../data/reference.json";
import { theoryFile, skills, skill } from "../data";
import type { TheorySection } from "../data/types";
import { PageHeader, Section, Callout } from "../components/Section";
import SourceImage from "../components/SourceImage";
import AbilityIcon from "../components/AbilityIcon";
import { Kbd } from "../components/badges";

interface RefSheet { key: string; title: string; desc: string; figures: { path: string; w: number; h: number }[]; }
const reference = referenceJson as unknown as { sheets: RefSheet[] };

function TheoryBlock({ s }: { s: TheorySection }) {
  return (
    <Section id={`theory-${s.id}`} title={s.title} desc={s.desc}>
      <div className="cards">
        {s.groups.map((g, gi) => (
          <div className="card" key={gi}>
            <h3>{g.label}</h3>
            {g.entries.length > 0 && (
              <ul>
                {g.entries.map((e, i) => {
                  const sk = skill(e.skill);
                  return (
                    <li key={i}>
                      <AbilityIcon id={e.skill} /> <b>{sk.name}</b> <Kbd>{e.input}</Kbd>
                      {e.note && <span className="why">{e.note}</span>}
                    </li>
                  );
                })}
              </ul>
            )}
            {g.pros && <p className="why" style={{ color: "var(--ok)" }}>+ {g.pros.join("; ")}</p>}
            {g.cons && <p className="why" style={{ color: "var(--none)" }}>− {g.cons.join("; ")}</p>}
          </div>
        ))}
      </div>
      {s.notes.map((n, i) => <p key={i} className="note">{n}</p>)}
    </Section>
  );
}

export default function ReferencePage() {
  const locked = skills.filter((s) => s.kind === "locked-only");
  const quickslot = skills.filter((s) => s.kind === "quick-slot");

  return (
    <>
      <PageHeader title="Reference">
        Guide overview, gearing and bug figures (source screenshots, not transcribed), PvP combo
        theory, and the lock / quick-slot lists.
      </PageHeader>

      {theoryFile.sections.map((s) => <TheoryBlock key={s.id} s={s} />)}

      <Section id="quickslot" title="Quick-slot skills" count={quickslot.length}>
        <div className="hotbar-row">
          {quickslot.map((s) => (
            <div className="hotbar-slot" key={s.id}>
              <div className="slot-name"><AbilityIcon id={s.id} size="row" />{s.name}</div>
              <p className="dim">{s.recommended_usage}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section id="locked" title="Skills to Lock" count={locked.length}
        desc="Recommended locks for newer players">
        <div className="hotbar-row">
          {locked.map((s) => (
            <div className="hotbar-slot" key={s.id}>
              <div className="slot-name"><AbilityIcon id={s.id} size="row" />{s.name}</div>
            </div>
          ))}
        </div>
        <p className="note">Some are user preference after you've learned the basics.</p>
      </Section>

      {reference.sheets.map((sh) => (
        <Section key={sh.key} id={`ref-${sh.key}`} title={sh.title} desc={sh.desc}
          count={sh.figures.length ? `${sh.figures.length} figures` : undefined}>
          {sh.key === "important-info" && (
            <Callout tag="SEE SKILLS">
              This sheet's per-skill protection, CC, and buff/debuff data is reflected on the{" "}
              <a href="#/skills">Skills</a> page and in combo category labels.
            </Callout>
          )}
          {sh.key === "class-bug-issues" && (
            <Callout tag="KNOWN BUG" warn>
              Skill Hit Delay (June 2023 patch): noticeable hit-lag, especially on Divina Inpulsa,
              Blitz Stab and Promptness — this is why the guide Q-block cancels most skills. See the
              source sheet for community video submissions.
            </Callout>
          )}
          <div style={{ display: "flex", flexWrap: "wrap", gap: 16 }}>
            {sh.figures.map((f) => <SourceImage key={f.path} path={f.path} alt={sh.title} />)}
          </div>
        </Section>
      ))}
    </>
  );
}
