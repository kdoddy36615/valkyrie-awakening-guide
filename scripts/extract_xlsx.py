"""Lossless extraction of the Valkyrie Guide 2026 spreadsheet into sources/.

Regenerates sources/ from docs/*.xlsx (no dependency on the throwaway Downloads staging).
Produces, for the awakening-relevant sheets only (Succession / Change Log / Placeholder are
out of scope per HANDOFF):

  sources/text/<sheet>.md          — every non-empty cell as "A1\tvalue" (utf-8, lossless)
  sources/images/<sheet>/*.png     — every embedded image, named <media>__<fromCell>.png
  sources/images/<sheet>/anchors.json — image -> {media, from/to col+row+cell} anchor map
  sources/comments.json            — cell comments (xl/comments1.xml; sheet "Awakening Tricks")
  sources/hyperlinks.json          — per-sheet cell -> url (from worksheet rels + <hyperlink>)

openpyxl's image paths are unreliable (HANDOFF), so images are read straight from the
drawing XML + drawing rels via zipfile — that is the authoritative icon->cell anchor source.
Console is cp1252; run with PYTHONIOENCODING=utf-8.
"""
import json
import re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
XLSX = ROOT / "docs" / "Valkyrie Guide 2026.xlsx"
SRC = ROOT / "sources"

# sheet display name -> worksheet file (resolved from workbook.xml at runtime); we only emit
# the awakening-relevant sheets.
IN_SCOPE = {
    "Introduction", "Important Info", "Gearing Guide",
    "Awakening (Combos, Add-ons)", "Awakening Tricks", "Awakening PvE DPS chart",
    "Class Bug & Issues",
}

NS_SS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def col_letter(n: int) -> str:
    """0-based column index -> spreadsheet letter (0->A)."""
    s = ""
    n += 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cell_ref(col0: int, row0: int) -> str:
    return f"{col_letter(col0)}{row0 + 1}"


def main():
    z = zipfile.ZipFile(XLSX)
    names = set(z.namelist())

    # ---- shared strings ----
    shared = []
    if "xl/sharedStrings.xml" in names:
        ss = z.read("xl/sharedStrings.xml").decode("utf-8")
        for si in re.findall(r"<si>(.*?)</si>", ss, re.S):
            texts = re.findall(r"<t(?:\s[^>]*)?>(.*?)</t>", si, re.S)
            shared.append("".join(texts))
    import html as htmllib
    shared = [htmllib.unescape(s) for s in shared]

    # ---- workbook: sheet name -> worksheet target ----
    wb = z.read("xl/workbook.xml").decode("utf-8")
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf-8")
    relmap = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', rels))
    sheets = []
    for m in re.finditer(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="(rId\d+)"', wb):
        nm = htmllib.unescape(m.group(1))
        sheets.append((nm, "xl/" + relmap[m.group(2)].lstrip("/")))

    for d in ("text", "images"):
        p = SRC / d
        if p.exists():
            shutil.rmtree(p)
        p.mkdir(parents=True)

    hyperlinks = {}
    comments_out = {}
    img_total = 0

    for name, wpath in sheets:
        if name not in IN_SCOPE:
            continue
        safe = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
        xml = z.read(wpath).decode("utf-8")

        # ---- cell text ----
        lines = [f"# {name}  ({wpath})", ""]
        # cells are either self-closing (<c r=".." s=".."/>) or have a body; match both and
        # never let a body span into the next cell (non-greedy, alternation tries /> first).
        for cm in re.finditer(r'<c r="([A-Z]+\d+)"([^>]*?)(?:/>|>(.*?)</c>)', xml, re.S):
            ref, attrs, body = cm.group(1), cm.group(2), cm.group(3)
            if body is None:  # self-closing / empty cell
                continue
            t = re.search(r't="([^"]+)"', attrs)
            ctype = t.group(1) if t else "n"
            vm = re.search(r"<v>(.*?)</v>", body, re.S)
            if ctype == "s" and vm:
                val = shared[int(vm.group(1))]
            elif ctype == "inlineStr":
                val = "".join(re.findall(r"<t(?:\s[^>]*)?>(.*?)</t>", body, re.S))
                val = htmllib.unescape(val)
            elif vm:
                val = htmllib.unescape(vm.group(1))
            else:
                continue
            val = val.replace("\r\n", "\n").replace("\n", "\\n").strip()
            if val:
                lines.append(f"{ref}\t{val}")
        (SRC / "text" / f"{safe}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

        # ---- hyperlinks ----
        wrels_path = "xl/worksheets/_rels/" + wpath.split("/")[-1] + ".rels"
        rid_url = {}
        if wrels_path in names:
            wr = z.read(wrels_path).decode("utf-8")
            rid_url = dict(re.findall(
                r'Id="(rId\d+)"[^>]*Target="([^"]+)"[^>]*TargetMode="External"', wr))
        hl = {}
        for hm in re.finditer(r"<hyperlink\b([^>]*)/?>", xml):
            attrs = hm.group(1)
            ref = re.search(r'ref="([^"]+)"', attrs)
            rid = re.search(r'r:id="(rId\d+)"', attrs)
            if ref and rid and rid.group(1) in rid_url:
                hl[ref.group(1)] = htmllib.unescape(rid_url[rid.group(1)])
        if hl:
            hyperlinks[name] = hl

        # ---- images via drawing XML + drawing rels ----
        dm = re.search(r'drawing\d+\.xml', xml)  # the <drawing r:id> points via rels
        drawing = None
        if wrels_path in names:
            wr = z.read(wrels_path).decode("utf-8")
            dmm = re.search(r'Target="([^"]*drawing\d+\.xml)"', wr)
            if dmm:
                drawing = "xl/" + dmm.group(1).replace("../", "")
        if drawing and drawing in names:
            dxml = z.read(drawing).decode("utf-8")
            drels_path = "xl/drawings/_rels/" + drawing.split("/")[-1] + ".rels"
            embed_media = {}
            if drels_path in names:
                dr = z.read(drels_path).decode("utf-8")
                embed_media = dict(re.findall(r'Id="(rId\d+)"[^>]*Target="([^"]+)"', dr))
            outdir = SRC / "images" / safe
            outdir.mkdir(parents=True, exist_ok=True)
            anchors = []
            # both one- and two-cell anchors
            for am in re.finditer(r"<xdr:(twoCellAnchor|oneCellAnchor)[^>]*>(.*?)</xdr:\1>",
                                  dxml, re.S):
                block = am.group(2)
                frm = re.search(r"<xdr:from>(.*?)</xdr:from>", block, re.S)
                to = re.search(r"<xdr:to>(.*?)</xdr:to>", block, re.S)

                def cr(seg):
                    c = re.search(r"<xdr:col>(\d+)</xdr:col>", seg)
                    r = re.search(r"<xdr:row>(\d+)</xdr:row>", seg)
                    return (int(c.group(1)) if c else None,
                            int(r.group(1)) if r else None)

                fc, fr = cr(frm.group(1)) if frm else (None, None)
                tc, tr = cr(to.group(1)) if to else (None, None)
                blip = re.search(r'<a:blip[^>]*r:embed="(rId\d+)"', block)
                if not blip or fc is None:
                    continue
                media = embed_media.get(blip.group(1), "")
                media_file = "xl/" + media.replace("../", "")
                from_cell = cell_ref(fc, fr)
                rec = {
                    "media": media.split("/")[-1],
                    "from_col": fc, "from_row": fr, "from_cell": from_cell,
                    "to_col": tc, "to_row": tr,
                    "to_cell": cell_ref(tc, tr) if tc is not None else None,
                }
                anchors.append(rec)
                if media_file in names:
                    ext = media.split(".")[-1]
                    base = rec["media"].rsplit(".", 1)[0]
                    dest = outdir / f"{base}__{from_cell}.{ext}"
                    if not dest.exists():
                        dest.write_bytes(z.read(media_file))
                        img_total += 1
            anchors.sort(key=lambda a: (a["from_row"], a["from_col"]))
            (outdir / "anchors.json").write_text(
                json.dumps(anchors, indent=2), encoding="utf-8")

    # ---- comments (xl/comments1.xml — the Awakening Tricks sheet) ----
    for cf in sorted(n for n in names if re.match(r"xl/comments\d+\.xml$", n)):
        cxml = z.read(cf).decode("utf-8")
        cl = {}
        for cm in re.finditer(r"<comment\b([^>]*)>(.*?)</comment>", cxml, re.S):
            ref = re.search(r'ref="([^"]+)"', cm.group(1))
            if not ref:
                continue
            text = "".join(re.findall(r"<t(?:\s[^>]*)?>(.*?)</t>", cm.group(2), re.S))
            text = htmllib.unescape(text).strip()
            if text:
                cl[ref.group(1)] = text
        if cl:
            comments_out[cf.split("/")[-1]] = cl

    (SRC / "hyperlinks.json").write_text(
        json.dumps(hyperlinks, indent=2, ensure_ascii=False), encoding="utf-8")
    (SRC / "comments.json").write_text(
        json.dumps(comments_out, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"extracted {img_total} images across in-scope sheets")
    print(f"hyperlinks: {sum(len(v) for v in hyperlinks.values())} in {len(hyperlinks)} sheets")
    print(f"comments: {sum(len(v) for v in comments_out.values())}")


if __name__ == "__main__":
    main()
