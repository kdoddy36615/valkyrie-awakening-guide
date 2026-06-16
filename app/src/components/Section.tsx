import type { ReactNode } from "react";

export function Section({ id, title, count, desc, children }:
  { id: string; title: string; count?: number | string; desc?: string; children: ReactNode }) {
  return (
    <section className="sec" id={id}>
      <div className="sechead">
        <h2>{title}</h2>
        {count != null && <span className="cnt">{count}</span>}
        {desc && <span className="d">{desc}</span>}
      </div>
      {children}
    </section>
  );
}

// Valkyrie has no global mode toggle — PageHeader is just an h1 + dim subtitle.
export function PageHeader({ title, children }: { title: string; children?: ReactNode }) {
  return (<><h1 className="h1">{title}</h1>{children && <p className="page-sub">{children}</p>}</>);
}

export function Callout({ tag, warn, children }: { tag?: string; warn?: boolean; children: ReactNode }) {
  return (
    <div className={warn ? "callout warn" : "callout"}>
      {tag && <span className="tag">{tag}</span>}
      <span>{children}</span>
    </div>
  );
}
