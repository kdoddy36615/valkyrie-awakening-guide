import { PageHeader, Callout } from "../components/Section";

export default function R1Page() {
  return (
    <>
      <PageHeader title="R1 AOS">
        Reserved area for Rank-1 Arena of Solare observations.
      </PageHeader>
      <Callout tag="PLANNED">
        This route is intentionally empty in v1. The dedicated AOS deep-dive is post-v1: logged
        records of watched Rank-1 Valkyrie play (skills + the order pressed) captured from replays —
        kept as a usage record, not a taught combo. The data schema reserves room for it now, so it
        drops in here without rework. See ADR 0003 and the [[Observation]] glossary entry.
      </Callout>
    </>
  );
}
