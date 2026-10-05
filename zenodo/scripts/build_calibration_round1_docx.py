"""Human Word packets for Calibration Round 1 (Daniel / Jose Jaime).

Natural academic Spanish. Same 20 cases, same order. No technical metadata.
"""

from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

ROOT = PROJECT_ROOT
PACKET_CSV = (
    DATA_PRIVATE / "calibration" / "round1" / "CALIBRATION_ROUND1_PACKET_BLINDED.csv"
)
OUT_DIR = ROOT / "_internal" / "calibration_round1"
CODEBOOK = PROTOCOL_DIR / "reply_status_codebook_v0.3.md"


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
    page_break_before=False,
):
    p = doc.add_paragraph()
    if align is not None:
        p.alignment = align
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.page_break_before = page_break_before
    run = p.add_run(text)
    set_run_font(run, size=size, bold=bold, italic=italic)
    return p


def add_heading_like(doc, text, size=16, space_before=10, page_break_before=False):
    return add_para(
        doc,
        text,
        size=size,
        bold=True,
        space_after=10,
        space_before=space_before,
        page_break_before=page_break_before,
    )


def add_label(doc, label):
    return add_para(doc, label, size=12, bold=True, space_after=4, space_before=10)


def add_body_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(10)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.left_indent = Cm(0.25)
    set_run_font(p.add_run(str(text).strip()), size=11)
    return p


def add_checkbox_line(doc, text):
    return add_para(doc, f"☐  {text}", size=12, space_after=6, space_before=2)


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


def add_comment_box(doc, height_cm: float = 2.8):
    table = doc.add_table(rows=1, cols=1)
    cell = table.cell(0, 0)
    set_cell_border(cell, val="single", sz="12", color="888888")
    set_row_height(table.rows[0], height_cm)
    cell.text = ""
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(6)
    set_run_font(p.add_run(" "), size=12)
    for _ in range(2):
        p2 = cell.add_paragraph()
        p2.paragraph_format.space_after = Pt(8)
        set_run_font(p2.add_run(" "), size=12)
    add_para(doc, "", size=6, space_after=4)


def clear_core_props(doc: Document, *, annotator: str) -> None:
    props = doc.core_properties
    props.author = ""
    props.last_modified_by = ""
    props.title = f"Calibración ronda 1 — {annotator}"
    props.subject = ""
    props.keywords = ""
    props.category = ""
    props.comments = ""


def add_instructions(doc: Document) -> None:
    doc.add_paragraph()
    add_para(
        doc,
        "Primera ronda de calibración",
        size=20,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        "Tipo de respuesta en las sesiones de control parlamentario",
        size=14,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=16,
    )
    add_para(
        doc,
        (
            "Esta es la primera ronda de calibración. Complete los veinte casos "
            "de forma independiente y no comente el contenido con la otra "
            "persona hasta que ambos documentos hayan sido devueltos."
        ),
        size=12,
        space_after=10,
    )
    add_para(
        doc,
        (
            "El juicio es lingüístico: se valora si la primera respuesta del "
            "Presidente del Gobierno atiende a la demanda comunicativa de la "
            "pregunta oral. No se valora la veracidad, la ideología ni la "
            "calidad política de lo dicho."
        ),
        size=12,
        space_after=10,
    )
    add_para(
        doc,
        (
            "Use la pregunta oral como objetivo principal del análisis. La "
            "pregunta registrada sirve de contexto institucional para "
            "interpretar qué se está preguntando."
        ),
        size=12,
        space_after=12,
    )

    add_heading_like(doc, "Categorías", size=14, space_before=4)
    add_para(
        doc,
        (
            "Respuesta explícita. La intervención resuelve de forma directa la "
            "demanda comunicativa principal."
        ),
        size=12,
        space_after=6,
    )
    add_para(
        doc,
        (
            "Respuesta parcial o intermedia. Atiende de forma sustantiva al "
            "menos a una parte de la demanda, pero deja otra parte relevante "
            "sin resolver, o exige una inferencia razonablemente acotada."
        ),
        size=12,
        space_after=6,
    )
    add_para(
        doc,
        (
            "Ausencia de respuesta. No aporta información sustantiva que "
            "atienda a la demanda, aunque hable del mismo tema general."
        ),
        size=12,
        space_after=10,
    )
    add_para(
        doc,
        (
            "Hablar del mismo tema no basta. Las referencias genéricas "
            "(por ejemplo, ley, medida, propuesta, fórmula) solo cuentan "
            "cuando la proposición aporta lo pedido."
        ),
        size=12,
        italic=True,
        space_after=12,
    )
    add_para(
        doc,
        (
            "Escriba observaciones solo si marca el caso como dudoso, si "
            "considera que falta algún criterio, o si hay otro problema "
            "genuino. No hace falta justificar todos los casos."
        ),
        size=12,
        space_after=8,
    )
    add_para(doc, "Número de casos: 20", size=12, bold=True, space_after=4)
    add_para(
        doc,
        "Tiempo estimado: entre 75 y 100 minutos, según la extensión de los textos.",
        size=12,
        space_after=8,
    )


def add_case(doc: Document, case_no: int, row) -> None:
    add_heading_like(
        doc, f"CASO {case_no}", size=18, space_before=0, page_break_before=True
    )
    add_label(doc, "Pregunta registrada")
    add_body_block(doc, row["registered_question"])
    add_label(doc, "Pregunta oral")
    add_body_block(doc, row["Q1"])
    add_label(doc, "Primera respuesta del Presidente del Gobierno")
    add_body_block(doc, row["R1"])

    add_label(doc, "Valoración")
    add_checkbox_line(doc, "Respuesta explícita")
    add_checkbox_line(doc, "Respuesta parcial o intermedia")
    add_checkbox_line(doc, "Ausencia de respuesta")

    add_label(doc, "Caso dudoso")
    add_checkbox_line(doc, "Sí")
    add_checkbox_line(doc, "No")

    add_label(doc, "Observaciones")
    add_comment_box(doc, height_cm=3.0)


def build_one(annotator_slug: str, display_name: str) -> Path:
    df = pd.read_csv(PACKET_CSV)
    assert len(df) == 20
    doc = Document()
    clear_core_props(doc, annotator=display_name)
    section = doc.sections[0]
    section.page_width = Cm(21.0)
    section.page_height = Cm(29.7)
    section.top_margin = Cm(2.0)
    section.bottom_margin = Cm(2.0)
    section.left_margin = Cm(2.2)
    section.right_margin = Cm(2.2)

    add_instructions(doc)
    for _, row in df.sort_values("case_no").iterrows():
        add_case(doc, int(row["case_no"]), row)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / f"calibracion_ronda1_{annotator_slug}.docx"
    doc.save(out)
    return out


def write_provenance(paths: dict[str, Path]) -> Path:
    codebook_hash = hashlib.sha256(CODEBOOK.read_bytes()).hexdigest()
    # companion copy of codebook for human use
    companion = OUT_DIR / "guia_tipo_de_respuesta_v0.3.md"
    shutil.copy2(CODEBOOK, companion)

    payload = {
        "phase": "5A",
        "round": 1,
        "codebook_version": "0.3.0",
        "codebook_sha256": codebook_hash,
        "codebook_companion": str(companion.relative_to(ROOT)),
        "packets": {
            name: {
                "path": str(path.relative_to(ROOT)),
                "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            }
            for name, path in paths.items()
        },
        "manifest_yaml": "zenodo/protocol/calibration_round1_manifest.yaml",
        "manifest_yaml_sha256": hashlib.sha256(
            (PROTOCOL_DIR / "calibration_round1_manifest.yaml").read_bytes()
        ).hexdigest(),
        "blinded_packet_csv": str(PACKET_CSV.relative_to(ROOT)),
        "blinded_packet_csv_sha256": hashlib.sha256(PACKET_CSV.read_bytes()).hexdigest(),
        "same_cases_same_order": True,
        "independence_rule": (
            "No discussion until both completed packets are returned; "
            "agreement calculated before discussion."
        ),
    }
    out = OUT_DIR / "CALIBRATION_ROUND1_PACKET_PROVENANCE.json"
    out.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return out


def main() -> int:
    daniel = build_one("Daniel", "Daniel Pinto Pajares")
    jose = build_one("Jose_Jaime", "Jose Jaime Baena Rojas")
    # byte-identical case content: rebuild jose from same builder path already
    # verify same case texts by hashing sorted case bodies via CSV
    prov = write_provenance({"daniel": daniel, "jose_jaime": jose})
    print(daniel)
    print(jose)
    print(prov)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
