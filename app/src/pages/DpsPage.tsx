import { dpsFile } from "../data";
import { PageHeader, Callout } from "../components/Section";
import DpsTable from "../components/DpsTable";

export default function DpsPage() {
  const { meta, rows } = dpsFile;
  return (
    <>
      <PageHeader title="DPS Chart">
        {meta.title} — {meta.author}. {meta.assumption}. Sortable; values are copied verbatim and
        never recomputed.
      </PageHeader>

      <Callout tag="LOCKED" warn>
        {meta.notes.join(" · ")}. {meta.locked_note}
      </Callout>

      <DpsTable rows={rows} />

      <p className="prov" style={{ marginTop: 12 }}>
        Source: {meta.source}. Cancel/combination rows (e.g. "Verdict Vult cancel",
        "Celestial Smite + abs. spear") are measurements mapped to their base skill, keeping the
        sheet label.
      </p>
    </>
  );
}
