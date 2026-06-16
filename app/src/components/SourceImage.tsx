import { useEffect, useState } from "react";

// Add-on screenshots live in app/src/assets/addons (copied by fetch_icons.py);
// reference figures live in sources/images. Glob both and resolve by the `path` prop:
//   "addons/sarron-pvp.png"  OR  "sources/images/important-info/imageNN__X.png"
const addons = import.meta.glob("../assets/addons/*.png", {
  eager: true, query: "?url", import: "default",
}) as Record<string, string>;
const sourceImgs = import.meta.glob("../../../sources/**/*.png", {
  eager: true, query: "?url", import: "default",
}) as Record<string, string>;

function resolve(p: string): string | undefined {
  if (p.startsWith("addons/")) return addons[`../assets/${p}`];
  return sourceImgs[`../../../${p}`];
}

export default function SourceImage({ path, alt }: { path: string; alt: string }) {
  const url = resolve(path);
  const [open, setOpen] = useState(false);
  useEffect(() => {
    if (!open) return;
    const onKey = (e: KeyboardEvent) => { if (e.key === "Escape") setOpen(false); };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);
  if (!url) return <p className="note">Missing image: {path}</p>;
  return (
    <>
      <figure className="thumb">
        <button type="button" onClick={() => setOpen(true)} title="Click to zoom">
          <img src={url} alt={alt} loading="lazy" />
        </button>
        <figcaption>{alt} — click to zoom</figcaption>
      </figure>
      {open && (
        <div className="lightbox" onClick={() => setOpen(false)} role="dialog" aria-label={alt}>
          <img src={url} alt={alt} />
        </div>
      )}
    </>
  );
}
