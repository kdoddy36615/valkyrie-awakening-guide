// Skill icons fetched from BDO Codex (scripts/fetch_icons.py), named by canonical skill id.
const icons = import.meta.glob("../assets/icons/*.webp", {
  eager: true, query: "?url", import: "default",
}) as Record<string, string>;

export function iconUrl(skillId: string): string | undefined {
  return icons[`../assets/icons/${skillId}.webp`];
}

export default function AbilityIcon({ id, size = "sm" }: { id: string; size?: "sm" | "row" | "xl" }) {
  const url = iconUrl(id);
  if (!url) return null; // unmatched icons are flagged in data, never block render
  return <img className={`ability-icon ${size}`} src={url} alt="" loading="lazy" />;
}
