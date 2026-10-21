#!/usr/bin/env python3
"""Build the requirement matrix.

    python3 build_matrix.py rows.json <client>_requirements.xlsx

rows.json is a list of objects. Every key is optional; missing ones render empty:

    [
      {"id": "R1",
       "source": "SoW response.xlsx / sheet 17 / row 24",
       "requirement": "Homepage should show customer feedback",
       "interpretation": "Testimonial carousel, client-maintained, unlimited entries",
       "origin": "Stated",
       "area": "Website",
       "verdict": "Custom",
       "evidence": "No standard testimonial model in 18.0 CE or EE",
       "hosting": "Data-only build; editable region leaves module control on first save",
       "effort": "M",
       "risk": "Real testimonials not yet supplied; FTC disclosure applies",
       "depends_on": "Client: 6-10 real testimonials with consent",
       "question": "Q4",
       "status": "New scope"}
    ]

Writes .xlsx when openpyxl is importable, otherwise .csv with the same columns, and
says which it did. No other dependencies.
"""
import json
import sys
import csv
import os

COLUMNS = [
    ("id",             "ID",                    8),
    ("source",         "Source",                34),
    ("requirement",    "Requirement (client)",  46),
    ("interpretation", "Interpretation",        46),
    ("origin",         "Stated / Inferred",     14),
    ("area",           "Area",                  16),
    ("verdict",        "Verdict",               16),
    ("evidence",       "Evidence",              40),
    ("hosting",        "Hosting impact",        34),
    ("effort",         "Effort",                8),
    ("risk",           "Risk",                  34),
    ("depends_on",     "Depends on",            30),
    ("question",       "Question",              10),
    ("status",         "Status",                14),
]

VERDICT_FILL = {
    "Standard":     "C6E7C6",   # green   — already there
    "Config":       "DCEAF7",   # blue    — setup only
    "App":          "E5DBF2",   # purple  — buy it
    "Custom":       "FDE9C9",   # amber   — build it
    "Not feasible": "F6C9C6",   # red     — cannot, as specified
    "Unclear":      "E8E8E8",   # grey    — blocked on a question
}


def _verdict_key(value):
    """Match a verdict to its colour.

    The prose name is "Not feasible as specified"; the column often carries the
    short form. Match on the longest key the value starts with, so both colour.
    """
    v = str(value or "").strip()
    for k in sorted(VERDICT_FILL, key=len, reverse=True):
        if v.lower().startswith(k.lower()):
            return k
    return None


def write_csv(rows, path):
    path = os.path.splitext(path)[0] + ".csv"
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([h for _, h, _ in COLUMNS])
        for r in rows:
            w.writerow([r.get(k, "") for k, _, _ in COLUMNS])
    return path


def write_xlsx(rows, path):
    from openpyxl import Workbook
    from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    from openpyxl.utils import get_column_letter

    wb = Workbook()
    ws = wb.active
    ws.title = "Requirements"

    head_fill = PatternFill("solid", fgColor="2E3B4E")
    head_font = Font(bold=True, color="FFFFFF", size=11)
    thin = Side(style="thin", color="D0D0D0")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    for i, (_, header, width) in enumerate(COLUMNS, start=1):
        c = ws.cell(row=1, column=i, value=header)
        c.fill, c.font, c.border = head_fill, head_font, border
        c.alignment = Alignment(vertical="center", wrap_text=True)
        ws.column_dimensions[get_column_letter(i)].width = width
    ws.row_dimensions[1].height = 30

    for ri, row in enumerate(rows, start=2):
        for ci, (key, _, _) in enumerate(COLUMNS, start=1):
            c = ws.cell(row=ri, column=ci, value=row.get(key, ""))
            c.alignment = Alignment(vertical="top", wrap_text=True)
            c.border = border
            if key == "verdict":
                fill = VERDICT_FILL.get(_verdict_key(row.get(key, "")))
                if fill:
                    c.fill = PatternFill("solid", fgColor=fill)
                    c.font = Font(bold=True)

    ws.freeze_panes = "C2"
    ws.auto_filter.ref = "A1:%s%d" % (
        get_column_letter(len(COLUMNS)), max(len(rows) + 1, 2))

    # Coverage summary, so the shape of the project is visible without reading.
    s = wb.create_sheet("Coverage")
    s.column_dimensions["A"].width = 18
    s.column_dimensions["B"].width = 10
    s.cell(row=1, column=1, value="Verdict").font = Font(bold=True)
    s.cell(row=1, column=2, value="Count").font = Font(bold=True)
    counts = {}
    for r in rows:
        v = str(r.get("verdict", "") or "(none)").strip()
        counts[v] = counts.get(v, 0) + 1
    # Flag anything that matched no known verdict, rather than colouring it grey
    # and letting a typo pass as a category.
    unknown = [v for v in counts if v != "(none)" and not _verdict_key(v)]
    for i, v in enumerate(sorted(counts, key=lambda k: -counts[k]), start=2):
        s.cell(row=i, column=1, value=v)
        s.cell(row=i, column=2, value=counts[v])
        fill = VERDICT_FILL.get(_verdict_key(v))
        if fill:
            s.cell(row=i, column=1).fill = PatternFill("solid", fgColor=fill)
    s.cell(row=len(counts) + 2, column=1, value="Total").font = Font(bold=True)
    s.cell(row=len(counts) + 2, column=2, value=len(rows)).font = Font(bold=True)

    wb.save(path)
    return path


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    with open(sys.argv[1], encoding="utf-8") as fh:
        rows = json.load(fh)
    if not isinstance(rows, list):
        print("rows.json must be a list of objects")
        return 2

    unknown = {k for r in rows for k in r} - {k for k, _, _ in COLUMNS}
    if unknown:
        print("WARNING: ignored unknown keys: %s" % ", ".join(sorted(unknown)))

    try:
        import openpyxl  # noqa: F401
    except ImportError:
        out = write_csv(rows, sys.argv[2])
        print("openpyxl not installed -> wrote %s (%d rows)." % (out, len(rows)))
        print("For the formatted workbook: pip install openpyxl, or use the "
              "session's spreadsheet skill.")
        return 0

    unknown_verdicts = sorted(
        {str(r.get("verdict", "")).strip() for r in rows
         if str(r.get("verdict", "")).strip() and not _verdict_key(r.get("verdict"))})
    if unknown_verdicts:
        print("WARNING: unrecognised verdicts (no colour applied): %s"
              % ", ".join(unknown_verdicts))

    out = write_xlsx(rows, sys.argv[2])
    print("Wrote %s (%d rows)." % (out, len(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
