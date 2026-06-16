import { tricksFile } from "../data";
import type { Trick, TrickType } from "../data/types";
import { PageHeader, Section } from "../components/Section";
import AbilityIcon from "../components/AbilityIcon";

const TYPE_TITLE: Record<TrickType, string> = {
  cancel: "Cancels", transition: "Transitions", movement: "Movement", macro: "Macros & Tips",
};
const TYPE_ORDER: TrickType[] = ["cancel", "transition", "movement", "macro"];

function TrickCard({ t }: { t: Trick }) {
  return (
    <div className="card" style={{ marginBottom: 10 }}>
      <h3 style={{ display: "flex", alignItems: "center", gap: 6 }}>
        {t.icons.map((id) => <AbilityIcon key={id} id={id} size="sm" />)}
        {t.name}
      </h3>
      {t.sequences.length > 0 && (
        <ul>
          {t.sequences.map((s, i) => <li key={i}><span className="mono">{s}</span></li>)}
        </ul>
      )}
      {t.rows && t.rows.length > 0 && (
        <table className="dps-table" style={{ marginTop: 4 }}>
          <thead><tr><th>Input</th><th>Protected?</th></tr></thead>
          <tbody>
            {t.rows.map((r, i) => (
              <tr key={i}><td className="mono">{r.input}</td><td>{r.protected}</td></tr>
            ))}
          </tbody>
        </table>
      )}
      {t.notes.map((n, i) => <p key={i} className="why" style={{ marginTop: 6 }}>{n}</p>)}
      {t.comment && <p className="prov" style={{ marginTop: 6 }}>📝 {t.comment}</p>}
      {t.video && <p className="prov"><a href={t.video} target="_blank" rel="noreferrer">video ▶</a></p>}
    </div>
  );
}

export default function TricksPage() {
  const tricks = tricksFile.tricks;
  return (
    <>
      <PageHeader title="Tricks">
        Skill cancels, weapon transitions, movement tech and macros from the Awakening Tricks tab.
        Arrow sequences (➔) and protection notes are verbatim from the guide.
      </PageHeader>

      {TYPE_ORDER.map((type) => {
        const items = tricks.filter((t) => t.type === type);
        if (!items.length) return null;
        return (
          <Section key={type} id={type} title={TYPE_TITLE[type]} count={items.length}>
            <div className="cards">
              {items.map((t) => <TrickCard key={t.id} t={t} />)}
            </div>
          </Section>
        );
      })}
    </>
  );
}
