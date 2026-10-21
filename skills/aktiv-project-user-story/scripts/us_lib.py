# -*- coding: utf-8 -*-
"""Reusable builder for user-story .docx files (Aktiv format).

Styling (extracted from the finalized US-01..US-04 docs):
  Font        : Poppins throughout
  Title       : 18pt, navy #1F3864, bold      -> "User Story N: <Title>"
  Section (h2): 13.5pt, navy #1F3864, bold     -> "1. Business Requirements"
  Feature (h3): 11.5pt, maroon #7B1F2B, bold   -> "2.1 <Feature>"
  Inline label: 10.5pt, navy #1F3864, bold     -> "Description:", "UI Elements:", ...
  Body/bullets: 10.5pt, grey #404040
  Shot caption: 9.5pt, maroon #7B1F2B, bold    -> "[ Annotated screenshot: ... ]"
  Page        : US Letter, margins L/R 1.25in, T/B 1in, page-number footer.

Usage:
    from us_lib import Story
    s = Story(5, "International Invoice")
    s.h2("1. Business Requirements")
    s.para("...")
    s.h3("2.1 Customs summary page")
    s.label("Description:", "A new first page ...")
    s.label("UI Elements:")
    s.table(["Column", "Source", "Notes"], [["Description", "line name", "..."]])
    s.img("/path/to/annotated.png")            # full text-column width
    s.label("Behavior:")
    s.bullets(["...", "..."])
    s.h2("4. Change Log")
    s.changelog()                               # standard first row
    s.save("user_stories/US-05_International_Invoice.docx")
"""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
from docx.shared import Pt, RGBColor, Inches, Cm

FONT = "Poppins"
NAVY = RGBColor(0x1F, 0x38, 0x64)
MAROON = RGBColor(0x7B, 0x1F, 0x2B)
BODY = RGBColor(0x40, 0x40, 0x40)
GREY = RGBColor(0x80, 0x80, 0x80)


class Story:
    def __init__(self, number, title):
        self.doc = Document()
        self._page_setup()
        self._footer()
        self.title(f"User Story {number}: {title}")

    # ---- page / footer -------------------------------------------------
    def _page_setup(self):
        sec = self.doc.sections[0]
        sec.page_width, sec.page_height = Inches(8.5), Inches(11)
        sec.left_margin = sec.right_margin = Inches(1.25)
        sec.top_margin = sec.bottom_margin = Inches(1)
        normal = self.doc.styles["Normal"].font
        normal.name = FONT
        normal.size = Pt(10.5)
        normal.color.rgb = BODY

    def _footer(self):
        p = self.doc.sections[0].footer.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run("Page ")
        self._field(run, "PAGE")
        for r in p.runs:
            r.font.name = FONT
            r.font.size = Pt(9)
            r.font.color.rgb = GREY

    def _field(self, run, code):
        # Insert a Word field (e.g. PAGE) after the given run.
        el = run._r
        for tag, val in (("begin", None), ("instrText", f" {code} "), ("end", None)):
            fld = OxmlElement("w:fldChar") if tag != "instrText" else OxmlElement("w:instrText")
            if tag == "instrText":
                fld.set(qn("xml:space"), "preserve")
                fld.text = val
            else:
                fld.set(qn("w:fldCharType"), tag)
            el.addnext(fld)
            el = fld

    # ---- run helper ----------------------------------------------------
    def _run(self, p, text, size, color, bold=False):
        r = p.add_run(text)
        r.font.name = FONT
        r.font.size = Pt(size)
        r.font.color.rgb = color
        r.font.bold = bold
        return r

    # ---- blocks --------------------------------------------------------
    def title(self, text):
        p = self.doc.add_paragraph()
        self._run(p, text, 18, NAVY, True)
        p.paragraph_format.space_after = Pt(10)
        return p

    def h2(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        self._run(p, text, 13.5, NAVY, True)
        return p

    def h3(self, text):
        p = self.doc.add_paragraph()
        p.paragraph_format.space_before = Pt(10)
        p.paragraph_format.space_after = Pt(3)
        self._run(p, text, 11.5, MAROON, True)
        return p

    def para(self, text):
        p = self.doc.add_paragraph()
        self._run(p, text, 10.5, BODY, False)
        return p

    def label(self, label, text=None):
        """Bold navy inline label, optionally followed by grey body text."""
        p = self.doc.add_paragraph()
        self._run(p, label + (" " if text else ""), 10.5, NAVY, True)
        if text:
            self._run(p, text, 10.5, BODY, False)
        return p

    def bullets(self, items):
        for it in items:
            p = self.doc.add_paragraph(style="List Bullet")
            self._run(p, it, 10.5, BODY, False)

    def table(self, headers, rows):
        t = self.doc.add_table(rows=1, cols=len(headers))
        t.style = "Table Grid"
        for i, h in enumerate(headers):
            cell = t.rows[0].cells[i]
            cell.paragraphs[0].clear()
            self._run(cell.paragraphs[0], h, 10, NAVY, True)
        for row in rows:
            cells = t.add_row().cells
            for i, val in enumerate(row):
                cells[i].paragraphs[0].clear()
                self._run(cells[i].paragraphs[0], str(val), 10, BODY, False)
        self.doc.add_paragraph()
        return t

    def shot(self, caption):
        """Text placeholder when no image is available yet."""
        p = self.doc.add_paragraph()
        self._run(p, f"[ Annotated screenshot: {caption} ]", 9.5, MAROON, True)
        return p

    def img(self, path, caption=None, width_cm=17.0):
        p = self.doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.add_run().add_picture(path, width=Cm(width_cm))
        if caption:
            c = self.doc.add_paragraph()
            c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            self._run(c, caption, 9.5, MAROON, True)
        return p

    def changelog(self, rows=None):
        rows = rows or [["1.0", "Original user story drafted and finalized."]]
        return self.table(["Version", "Change Description"], rows)

    def save(self, path):
        self.doc.save(path)
        return path
