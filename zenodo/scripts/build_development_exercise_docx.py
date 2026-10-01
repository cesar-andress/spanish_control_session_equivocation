"""Build human-friendly development annotation DOCX for expert linguists."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "_internal" / "development" / "development_annotator_A.xlsx"
OUT_DOCX = ROOT / "_internal" / "development" / "Reply_Status_Development_Exercise.docx"


def set_run_font(run, *, size=12, bold=False, italic=False, name="Times New Roman"):
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), name)
    run.font.size = Pt(size)
    run.bold = bold
    run.italic = italic


def add_para(
    doc,
    text,
    *,
    size=12,
    bold=False,
    italic=False,
    space_after=8,
    space_before=0,
    align=None,
    first_line_indent=None,
):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.15
    if first_line_indent is not None:
        p.paragraph_format.first_line_indent = first_line_indent
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def add_heading_like(doc, text, size=16, space_before=10):
    return add_para(
        doc, text, size=size, bold=True, space_after=10, space_before=space_before
    )


def add_label(doc, label, *, size=12):
    return add_para(doc, label, size=size, bold=True, space_after=4, space_before=10)


def add_body_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.left_indent = Cm(0.25)
    run = p.add_run(str(text).strip())
    set_run_font(run, size=11)
    return p


def add_checkbox_line(doc, text):
    return add_para(doc, f"☐  {text}", size=12, space_after=6, space_before=2)


def set_cell_shading(cell, fill: str):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), fill)
    tcPr.append(shd)


def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement("w:tcBorders")
    for edge in ("top", "left", "bottom", "right"):
        element = OxmlElement(f"w:{edge}")
        element.set(qn("w:val"), kwargs.get("val", "single"))
        element.set(qn("w:sz"), kwargs.get("sz", "12"))
        element.set(qn("w:space"), "0")
        element.set(qn("w:color"), kwargs.get("color", "666666"))
        tcBorders.append(element)
    tcPr.append(tcBorders)


def set_row_height(row, cm_height: float):
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trHeight = OxmlElement("w:trHeight")
    trHeight.set(qn("w:val"), str(int(cm_height * 567)))
    trHeight.set(qn("w:hRule"), "atLeast")
    trPr.append(trHeight)


def prevent_row_split(row) -> None:
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    cant_split = OxmlElement("w:cantSplit")
    trPr.append(cant_split)


def add_boxed_category(doc, title: str, meaning: str, examples: list[str], note: str | None = None):
    table = doc.add_table(rows=1, cols=1)
    prevent_row_split(table.rows[0])
    cell = table.cell(0, 0)
    set_cell_border(cell, val="single", sz="14", color="555555")
    set_cell_shading(cell, "F7F7F7")
    cell.text = ""

    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.space_before = Pt(4)
    run = p.add_run(title)
    set_run_font(run, size=12, bold=True)

    p2 = cell.add_paragraph()
    p2.paragraph_format.space_after = Pt(3)
    run2 = p2.add_run(meaning)
    set_run_font(run2, size=11)

    p3 = cell.add_paragraph()
    p3.paragraph_format.space_after = Pt(1)
    run3 = p3.add_run("Examples:")
    set_run_font(run3, size=11, bold=True)

    for ex in examples:
        pe = cell.add_paragraph()
        pe.paragraph_format.space_after = Pt(0)
        pe.paragraph_format.left_indent = Cm(0.3)
        re_ = pe.add_run(f"• {ex}")
        set_run_font(re_, size=11)

    if note:
        pn = cell.add_paragraph()
        pn.paragraph_format.space_before = Pt(3)
        pn.paragraph_format.space_after = Pt(4)
        rn = pn.add_run(note)
        set_run_font(rn, size=11, italic=True)

    add_para(doc, "", size=6, space_after=6)


def add_comment_box(doc, height_cm: float = 4.0, *, label: str | None = "Comments"):
    if label:
        add_label(doc, label)
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    set_cell_border(cell, val="single", sz="12", color="888888")
    set_row_height(table.rows[0], height_cm)
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(8)
    run = p.add_run(" ")
    set_run_font(run, size=12)
    for _ in range(4):
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(10)
        set_run_font(p2.add_run(" "), size=12)
    add_para(doc, "", size=8, space_after=4)


def clear_core_props(doc: Document) -> None:
    props = doc.core_properties
    props.author = ""
    props.last_modified_by = ""
    props.title = "Pilot Annotation Exercise: Reply Status"
    props.subject = ""
    props.keywords = ""
    props.category = ""
    props.comments = ""


def add_instructions(doc: Document) -> None:
    for _ in range(1):
        doc.add_paragraph()

    add_para(
        doc,
        "Pilot Annotation Exercise:",
        size=22,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        "Reply Status in Spanish Parliamentary Control Sessions",
        size=16,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=18,
    )

    add_para(
        doc,
        (
            "The purpose of this exercise is to test whether preliminary annotation "
            "rules allow experts to classify parliamentary responses consistently. "
            "This is not the final annotation stage and no individual answer will be "
            "considered correct or incorrect. The objective is to identify ambiguous "
            "cases and improve the guidelines."
        ),
        size=12,
        space_after=12,
    )
    add_para(
        doc,
        (
            "Please work independently. Disagreement between experts is expected and "
            "useful. After the fifteen cases, complete the short feedback page at the "
            "end of this booklet."
        ),
        size=12,
        space_after=10,
    )
    add_para(doc, "Number of cases: 15", size=12, bold=True, space_after=4)
    add_para(
        doc,
        "Estimated time: about 60–90 minutes, depending on case length.",
        size=12,
        space_after=12,
    )

    doc.add_page_break()

    add_heading_like(doc, "Instructions", size=18, space_before=0)

    add_heading_like(doc, "What you are judging", size=14)
    add_para(
        doc,
        (
            "The annotator must decide whether the Prime Minister’s first response "
            "answers the question asked by the parliamentarian."
        ),
        size=12,
        space_after=8,
    )
    add_para(
        doc,
        (
            "Each case presents three texts: the registered written question, the "
            "oral question as spoken in the chamber, and the Prime Minister’s first "
            "response. The evaluation concerns the relation:"
        ),
        size=12,
        space_after=6,
    )
    add_para(
        doc,
        "QUESTION  →  FIRST RESPONSE",
        size=12,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
    )
    add_para(
        doc,
        (
            "Use the registered question as institutional context when the spoken "
            "turn is elliptical or refers back to it. The main object of judgement "
            "is whether the first response answers the oral question."
        ),
        size=12,
        space_after=10,
    )

    add_heading_like(doc, "What you are not judging", size=14)
    add_para(doc, "The evaluation does NOT concern:", size=12, space_after=4)
    not_items = [
        "whether the answer is politically convincing;",
        "whether the answer is factually true;",
        "whether you agree with the response;",
        "whether the question is fair;",
        "whether the government policy is good or bad.",
    ]
    for item in not_items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        set_run_font(p.add_run(item), size=12)

    add_para(doc, "", size=8, space_after=6)
    doc.add_page_break()
    add_heading_like(doc, "The three categories", size=14, space_before=0)

    add_boxed_category(
        doc,
        "EXPLICIT REPLY",
        "The response directly addresses the main issue raised in the oral question.",
        [
            "provides the requested information;",
            "confirms or denies the proposition;",
            "rejects a premise but still addresses it.",
        ],
        note=(
            "Important: a response does not need to agree with the question to count "
            "as an explicit reply."
        ),
    )
    add_boxed_category(
        doc,
        "INTERMEDIATE REPLY",
        "The response engages with the question but only partially or indirectly.",
        [
            "answers one part of a multi-part question;",
            "provides related information but does not fully address the main point;",
            "gives a response where the connection requires interpretation.",
        ],
    )
    add_boxed_category(
        doc,
        "NON-REPLY",
        "The response does not substantially address the question asked.",
        [
            "changes to an unrelated topic;",
            "discusses general achievements without addressing the question;",
            "attacks the questioner without answering the issue.",
        ],
    )

    doc.add_page_break()
    add_heading_like(doc, "How to decide", size=16, space_before=0)
    add_para(
        doc,
        "Use this short procedure for every case:",
        size=12,
        space_after=8,
    )
    steps = [
        ("Step 1.", "Identify the main issue in the oral question."),
        ("Step 2.", "Ask whether the first response addresses that issue."),
        ("Step 3.", "If clearly yes: Explicit reply."),
        ("Step 4.", "If partly or indirectly: Intermediate reply."),
        ("Step 5.", "If no meaningful answer: Non-reply."),
    ]
    for title, body in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r1 = p.add_run(f"{title} ")
        set_run_font(r1, size=12, bold=True)
        r2 = p.add_run(body)
        set_run_font(r2, size=12)

    add_para(doc, "", size=8, space_after=6)
    add_heading_like(doc, "Further guidance", size=14)
    bullets = [
        "Criticism of the questioner may appear together with an answer; if the issue is still addressed, that can be an explicit reply.",
        "If a case feels close to a category boundary, mark it as borderline and explain why in the comments.",
        "Judge only the first response printed in the case, not later turns.",
        "Disagreement between experts is informative for improving the guidelines.",
    ]
    for b in bullets:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(4)
        set_run_font(p.add_run(b), size=12)

    add_para(doc, "", size=8, space_after=6)
    add_heading_like(doc, "How to fill each case", size=14)
    add_para(
        doc,
        (
            "Read the three texts. Then, on the judgement page for that case, tick "
            "exactly one category, tick whether the case felt borderline, and use "
            "the comments box whenever the decision was difficult."
        ),
        size=12,
        space_after=8,
    )


def add_case(doc: Document, case_no: int, row) -> None:
    doc.add_page_break()
    add_heading_like(doc, f"CASE {case_no}", size=18, space_before=0)

    add_label(doc, "REGISTERED QUESTION")
    add_body_block(doc, row["registered_question"])

    add_label(doc, "ORAL QUESTION (Q1)")
    add_body_block(doc, row["Q1"])

    add_label(doc, "FIRST RESPONSE OF THE PRIME MINISTER (R1)")
    add_body_block(doc, row["R1"])

    doc.add_page_break()
    add_heading_like(doc, f"CASE {case_no} — YOUR DECISION", size=16, space_before=0)
    add_para(
        doc,
        "Choose one category. Then say whether this case felt borderline.",
        size=11,
        italic=True,
        space_after=10,
    )

    add_label(doc, "YOUR DECISION")
    add_checkbox_line(doc, "Explicit reply")
    add_checkbox_line(doc, "Intermediate reply")
    add_checkbox_line(doc, "Non-reply")

    add_label(doc, "BORDERLINE CASE")
    add_checkbox_line(doc, "Yes")
    add_checkbox_line(doc, "No")

    add_comment_box(doc, height_cm=8.0, label="COMMENTS")


def add_feedback(doc: Document) -> None:
    doc.add_page_break()
    add_heading_like(doc, "Feedback on the guidelines", size=18, space_before=0)
    add_para(
        doc,
        (
            "Please answer briefly after completing the fifteen cases. This feedback "
            "helps improve the coding guide. It is not a score for your decisions."
        ),
        size=12,
        space_after=12,
    )
    questions = [
        "1. Was the category decision clear overall?",
        "2. What rule, if any, felt missing?",
        "3. What wording in the instructions caused uncertainty?",
        "4. Would another expert in your field likely make the same decisions? Why or why not?",
        "5. Optional: which case numbers were hardest, and why?",
    ]
    for q in questions:
        add_para(doc, q, size=12, bold=True, space_after=6, space_before=8)
        add_comment_box(doc, height_cm=3.0, label=None)

    add_para(doc, "", size=8, space_after=8)
    add_para(
        doc,
        "Thank you for your time and careful judgement.",
        size=12,
        italic=True,
        space_after=6,
    )


def build() -> Path:
    df = pd.read_excel(SRC, sheet_name="CODING")
    assert len(df) == 15

    doc = Document()
    clear_core_props(doc)

    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

    add_instructions(doc)
    for i, row in df.iterrows():
        add_case(doc, int(i) + 1, row)
    add_feedback(doc)

    OUT_DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc.save(OUT_DOCX)
    return OUT_DOCX


if __name__ == "__main__":
    print(build())
