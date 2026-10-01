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
    run3 = p3.add_run("Ejemplos:")
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


def add_comment_box(doc, height_cm: float = 4.0, *, label: str | None = "Observaciones"):
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
    props.title = "Ejercicio inicial de revisión de criterios: tipo de respuesta"
    props.subject = ""
    props.keywords = ""
    props.category = ""
    props.comments = ""


def add_instructions(doc: Document) -> None:
    for _ in range(1):
        doc.add_paragraph()

    add_para(
        doc,
        "Ejercicio inicial de revisión de criterios",
        size=20,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        "Tipo de respuesta en las sesiones de control parlamentario",
        size=15,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=6,
    )
    add_para(
        doc,
        "Congreso de los Diputados · intervenciones del presidente del Gobierno",
        size=11,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=18,
    )

    add_para(
        doc,
        (
            "El objetivo de este ejercicio es comprobar si unos criterios "
            "preliminares de anotación permiten a expertos clasificar de forma "
            "coherente las respuestas parlamentarias. No se trata de la etapa "
            "final de anotación y ninguna respuesta individual se considerará "
            "correcta o incorrecta. La finalidad es identificar casos ambiguos "
            "y mejorar la guía de criterios."
        ),
        size=12,
        space_after=12,
    )
    add_para(
        doc,
        (
            "Trabaje de forma independiente. El desacuerdo entre expertos es "
            "esperado y útil. Al terminar los quince casos, complete la página "
            "final de observaciones."
        ),
        size=12,
        space_after=10,
    )
    add_para(doc, "Número de casos: 15", size=12, bold=True, space_after=4)
    add_para(
        doc,
        "Tiempo estimado: entre 60 y 90 minutos, según la extensión de los textos.",
        size=12,
        space_after=12,
    )

    doc.add_page_break()

    add_heading_like(doc, "Instrucciones", size=18, space_before=0)

    add_heading_like(doc, "Qué debe valorar", size=14)
    add_para(
        doc,
        (
            "La persona anotadora debe decidir si la primera respuesta del "
            "presidente del Gobierno contesta a la pregunta formulada por el "
            "diputado o la diputada."
        ),
        size=12,
        space_after=8,
    )
    add_para(
        doc,
        (
            "Cada caso presenta tres textos: la pregunta escrita registrada, la "
            "pregunta oral pronunciada en el hemiciclo y la primera respuesta "
            "del presidente del Gobierno. La evaluación se centra en la relación:"
        ),
        size=12,
        space_after=6,
    )
    add_para(
        doc,
        "PREGUNTA  →  PRIMERA RESPUESTA",
        size=12,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
    )
    add_para(
        doc,
        (
            "Utilice la pregunta registrada como contexto institucional cuando "
            "el turno oral sea elíptico o remita a ella. El objeto principal de "
            "juicio es si la primera respuesta contesta a la pregunta oral."
        ),
        size=12,
        space_after=10,
    )

    add_heading_like(doc, "Qué no debe valorar", size=14)
    add_para(doc, "La evaluación no se refiere a:", size=12, space_after=4)
    not_items = [
        "si la respuesta resulta políticamente convincente;",
        "si la respuesta es fácticamente verdadera;",
        "si usted está de acuerdo con lo dicho;",
        "si la pregunta es justa o sesgada;",
        "si la política del Gobierno es buena o mala.",
    ]
    for item in not_items:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(3)
        set_run_font(p.add_run(item), size=12)

    add_para(doc, "", size=8, space_after=6)
    doc.add_page_break()
    add_heading_like(doc, "Las tres categorías (tipo de respuesta)", size=14, space_before=0)

    add_boxed_category(
        doc,
        "RESPUESTA EXPLÍCITA",
        "La respuesta aborda de forma directa la cuestión principal planteada en la pregunta oral.",
        [
            "aporta la información solicitada;",
            "confirma o niega la proposición;",
            "rechaza una premisa, pero sigue abordándola.",
        ],
        note=(
            "Importante: una respuesta no necesita coincidir con el punto de vista "
            "del preguntante para considerarse respuesta explícita."
        ),
    )
    add_boxed_category(
        doc,
        "RESPUESTA PARCIAL O INTERMEDIA",
        "La respuesta se ocupa de la pregunta, pero solo de forma parcial o indirecta.",
        [
            "contesta a una parte de una pregunta con varios puntos;",
            "aporta información relacionada, sin abordar del todo el núcleo de la pregunta;",
            "ofrece una respuesta cuya conexión con la pregunta exige interpretación.",
        ],
    )
    add_boxed_category(
        doc,
        "AUSENCIA DE RESPUESTA",
        "La respuesta no aborda de manera sustancial la pregunta formulada.",
        [
            "cambia a un tema no relacionado;",
            "habla de logros generales sin atender a la pregunta;",
            "ataca a quien pregunta sin responder a la cuestión.",
        ],
    )

    doc.add_page_break()
    add_heading_like(doc, "Cómo decidir", size=16, space_before=0)
    add_para(
        doc,
        "Siga este procedimiento breve en cada caso:",
        size=12,
        space_after=8,
    )
    steps = [
        ("Paso 1.", "Identifique la cuestión principal de la pregunta oral."),
        ("Paso 2.", "Pregúntese si la primera respuesta aborda esa cuestión."),
        ("Paso 3.", "Si la respuesta es claramente sí: respuesta explícita."),
        ("Paso 4.", "Si lo hace solo en parte o de forma indirecta: respuesta parcial o intermedia."),
        ("Paso 5.", "Si no hay una contestación significativa: ausencia de respuesta."),
    ]
    for title, body in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        r1 = p.add_run(f"{title} ")
        set_run_font(r1, size=12, bold=True)
        r2 = p.add_run(body)
        set_run_font(r2, size=12)

    add_para(doc, "", size=8, space_after=6)
    add_heading_like(doc, "Orientaciones adicionales", size=14)
    bullets = [
        "Puede haber crítica a quien pregunta junto con una contestación; si la cuestión queda abordada, puede tratarse de una respuesta explícita.",
        "Si el caso se sitúa cerca del límite entre categorías, márquelo como caso dudoso y explique el motivo en las observaciones.",
        "Valore únicamente la primera respuesta impresa en el caso, no turnos posteriores.",
        "El desacuerdo entre expertos es informativo para mejorar la guía de criterios.",
    ]
    for b in bullets:
        p = doc.add_paragraph(style="List Bullet")
        p.paragraph_format.space_after = Pt(4)
        set_run_font(p.add_run(b), size=12)

    add_para(doc, "", size=8, space_after=6)
    add_heading_like(doc, "Cómo completar cada caso", size=14)
    add_para(
        doc,
        (
            "Lea los tres textos. A continuación, en la página de decisión de ese "
            "caso, marque exactamente una categoría, indique si el caso le resultó "
            "dudoso y use el recuadro de observaciones cuando la decisión haya sido "
            "difícil."
        ),
        size=12,
        space_after=8,
    )


def add_case(doc: Document, case_no: int, row) -> None:
    doc.add_page_break()
    add_heading_like(doc, f"CASO {case_no}", size=18, space_before=0)

    add_label(doc, "PREGUNTA REGISTRADA")
    add_body_block(doc, row["registered_question"])

    add_label(doc, "PREGUNTA ORAL")
    add_body_block(doc, row["Q1"])

    add_label(doc, "PRIMERA RESPUESTA DEL PRESIDENTE DEL GOBIERNO")
    add_body_block(doc, row["R1"])

    doc.add_page_break()
    add_heading_like(doc, f"CASO {case_no} — SU DECISIÓN", size=16, space_before=0)
    add_para(
        doc,
        "Elija una sola categoría. Indique después si el caso le resultó dudoso.",
        size=11,
        italic=True,
        space_after=10,
    )

    add_label(doc, "TIPO DE RESPUESTA")
    add_checkbox_line(doc, "Respuesta explícita")
    add_checkbox_line(doc, "Respuesta parcial o intermedia")
    add_checkbox_line(doc, "Ausencia de respuesta")

    add_label(doc, "CASO DUDOSO")
    add_checkbox_line(doc, "Sí")
    add_checkbox_line(doc, "No")

    add_comment_box(doc, height_cm=8.0, label="OBSERVACIONES")


def add_feedback(doc: Document) -> None:
    doc.add_page_break()
    add_heading_like(doc, "Observaciones sobre la guía de criterios", size=18, space_before=0)
    add_para(
        doc,
        (
            "Responda brevemente al terminar los quince casos. Estas observaciones "
            "sirven para mejorar la guía de criterios de anotación. No constituyen "
            "una puntuación de sus decisiones."
        ),
        size=12,
        space_after=12,
    )
    questions = [
        "1. ¿Le resultó clara, en conjunto, la decisión sobre las categorías?",
        "2. ¿Qué criterio, si alguno, echa en falta?",
        "3. ¿Qué formulación de las instrucciones le generó incertidumbre?",
        "4. ¿Cree que otro experto de su ámbito tomaría, en lo esencial, las mismas decisiones? ¿Por qué?",
        "5. Opcional: ¿qué números de caso le resultaron más difíciles y por qué?",
    ]
    for q in questions:
        add_para(doc, q, size=12, bold=True, space_after=6, space_before=8)
        add_comment_box(doc, height_cm=3.0, label=None)

    add_para(doc, "", size=8, space_after=8)
    add_para(
        doc,
        "Gracias por su tiempo y por su juicio cuidadoso.",
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
