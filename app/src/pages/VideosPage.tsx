import { videosFile } from "../data";
import { PageHeader, Section } from "../components/Section";

function host(url: string): string {
  if (/youtu\.be|youtube\.com/.test(url)) return "YouTube";
  if (/streamable\.com/.test(url)) return "Streamable";
  if (/discord\.gg|discord\.com/.test(url)) return "Discord";
  if (/playblackdesert/.test(url)) return "Patch Notes";
  return "Link";
}

export default function VideosPage() {
  return (
    <>
      <PageHeader title="Videos">
        Every video and link from the Discord guides and the spreadsheet, cited by author. Deduped so
        each link appears once. {videosFile.meta.count} links.
      </PageHeader>

      {videosFile.groups.map((g) => (
        <Section key={g.title} id={g.title.replace(/\W+/g, "-").toLowerCase()} title={g.title}
          count={g.videos.length} desc={g.note}>
          <ul className="notes" style={{ maxWidth: 920 }}>
            {g.videos.map((v, i) => (
              <li key={i} style={{ display: "flex", gap: 8, alignItems: "baseline", flexWrap: "wrap" }}>
                <a href={v.url} target="_blank" rel="noreferrer">{v.label}</a>
                <span className="badge optional">{host(v.url)}</span>
                <span className="dim" style={{ fontSize: 11.5 }}>— {v.author}</span>
              </li>
            ))}
          </ul>
        </Section>
      ))}
    </>
  );
}
