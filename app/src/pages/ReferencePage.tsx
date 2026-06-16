import referenceJson from "../../../data/reference.json";
import { theoryFile, buffsFile, skill, maybeSkill } from "../data";
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
  return (
    <>
      <PageHeader title="Reference">
        Guide overview, gearing and bug figures (source screenshots, not transcribed), and PvP combo
        theory. Loadout (core / Rabams / add-ons / locks) lives on the Setup pages.
      </PageHeader>

      {theoryFile.sections.map((s) => <TheoryBlock key={s.id} s={s} />)}

      <Section id="buffs" title="Important Skill Buffs" count={buffsFile.buffs.length}
        desc="Most important buffs only — each skill may have more (read the tooltips)">
        <div className="cards">
          {buffsFile.buffs.map((b, i) => {
            const ids = b.skills ?? (b.skill ? [b.skill] : []);
            const heading = b.name ?? (b.skill ? skill(b.skill).name : "Buff");
            return (
              <div className="card" key={i}>
                <h3 style={{ display: "flex", alignItems: "center", gap: 6 }}>
                  {ids.map((id) => maybeSkill(id) && <AbilityIcon key={id} id={id} size="sm" />)}
                  {heading}
                </h3>
                <p>{b.text}</p>
              </div>
            );
          })}
        </div>
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
