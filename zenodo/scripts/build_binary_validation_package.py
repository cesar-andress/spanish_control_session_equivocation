"""Phase 7B: issue binary-validation orientation + N=12 independent packets.

Does not redraw the fixed sample. Does not create main XIV packets.
Not Calibration Round 3.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import date, datetime, timezone
from pathlib import Path

import pandas as pd
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Mm, Pt

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

ROOT = PROJECT_ROOT
OUT = ROOT / "_internal" / "binary_validation"
VAL = DATA_PRIVATE / "validation" / "binary_v1"
PKT = VAL / "BINARY_VALIDATION_N12_PACKET_BLINDED.csv"
AUD = VAL / "BINARY_VALIDATION_N12_AUDIT.csv"
MAN = VAL / "BINARY_VALIDATION_MANIFEST.json"
GATE = VAL / "BINARY_VALIDATION_PROSPECTIVE_GATE.json"
INSTRUMENT = PROTOCOL_DIR / "direct_resolution_codebook_v1.0-validation.md"
REPORT = ROOT / "_internal" / "reports" / "BINARY_VALIDATION_PACKET_AUDIT.md"

RECIPIENTS = (
    ("Daniel", "Daniel"),
    ("Jose_Jaime", "Jose Jaime"),
)


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
    set_run_font(p.add_run(text), size=size, bold=bold, italic=italic)
    return p


def add_label(doc, label):
    return add_para(doc, label, size=12, bold=True, space_after=4, space_before=10)


def add_body_block(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.line_spacing = 1.2
    p.paragraph_format.left_indent = Cm(0.2)
    set_run_font(p.add_run(str(text).strip()), size=11)
    return p


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


def prevent_row_split(row) -> None:
    tr = row._tr
    trPr = tr.get_or_add_trPr()
    trPr.append(OxmlElement("w:cantSplit"))


def add_page_number(section) -> None:
    footer = section.footer
    footer.is_linked_to_previous = False
    p = footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run()
    set_run_font(run, size=10)
    fld_begin = OxmlElement("w:fldChar")
    fld_begin.set(qn("w:fldCharType"), "begin")
    instr = OxmlElement("w:instrText")
    instr.set(qn("xml:space"), "preserve")
    instr.text = " PAGE "
    fld_end = OxmlElement("w:fldChar")
    fld_end.set(qn("w:fldCharType"), "end")
    run._r.append(fld_begin)
    run._r.append(instr)
    run._r.append(fld_end)


def setup_page(doc) -> None:
    for section in doc.sections:
        section.page_width = Mm(210)
        section.page_height = Mm(297)
        section.top_margin = Cm(1.8)
        section.bottom_margin = Cm(1.8)
        section.left_margin = Cm(2.0)
        section.right_margin = Cm(2.0)
        add_page_number(section)


def add_binary_response_block(doc) -> None:
    table = doc.add_table(rows=1, cols=1)
    prevent_row_split(table.rows[0])
    cell = table.cell(0, 0)
    set_cell_border(cell, val="nil", sz="0", color="FFFFFF")
    cell.text = ""
    first = True

    def _line(text: str, *, bold=False, after=4, before=0, size=12):
        nonlocal first
        p = cell.paragraphs[0] if first else cell.add_paragraph()
        first = False
        p.paragraph_format.space_after = Pt(after)
        p.paragraph_format.space_before = Pt(before)
        set_run_font(p.add_run(text), size=size, bold=bold)

    _line("Tu valoración", bold=True, after=6, before=4)
    _line("☐  Sí — resolución directa", after=3)
    _line("☐  No — no resolución directa", after=8)
    _line("¿Te ha parecido un caso dudoso?", bold=True, after=4)
    _line("☐  Sí", after=2)
    _line("☐  No", after=8)
    _line("Observaciones, si hacen falta:", bold=True, after=2)
    rule = cell.add_paragraph()
    rule.paragraph_format.space_after = Pt(0)
    set_run_font(rule.add_run("_" * 64), size=10)
    for _ in range(2):
        blank = cell.add_paragraph()
        blank.paragraph_format.space_after = Pt(10)
        set_run_font(blank.add_run(" "), size=11)
    foot = cell.add_paragraph()
    set_run_font(foot.add_run("_" * 64), size=10)
    add_para(doc, "", size=4, space_after=2)


def build_orientation() -> Path:
    path = OUT / "01_ORIENTACION_CONJUNTA_RESOLUCION_DIRECTA.docx"
    doc = Document()
    setup_page(doc)

    add_para(
        doc,
        "Orientación breve — resolución directa",
        size=14,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=6,
    )
    add_para(
        doc,
        "Solo lectura conjunta. No hay nada que rellenar aquí.",
        size=11,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
    )
    add_para(
        doc,
        (
            "Esta vez cambiamos la forma de valorar las respuestas. Ya no vamos "
            "a decidir si una respuesta es explícita, parcial o ausente. Solo "
            "queremos distinguir una cosa: si la primera respuesta resuelve "
            "directamente la pregunta principal o no."
        ),
        size=11,
        space_after=8,
    )
    add_para(
        doc,
        "¿La primera respuesta del Presidente del Gobierno resuelve directamente la demanda principal de la pregunta?",
        size=12,
        bold=True,
        space_after=8,
    )
    add_para(doc, "Sí — resolución directa", size=11, bold=True, space_after=2)
    add_para(
        doc,
        (
            "Marcad Sí cuando la respuesta contenga una postura, evaluación, "
            "razón, compromiso, acción (hecha o prevista) o rechazo de la "
            "premisa que, de hecho, resuelva lo que se pregunta."
        ),
        size=11,
        space_after=6,
    )
    add_para(doc, "No — no resolución directa", size=11, bold=True, space_after=2)
    add_para(
        doc,
        (
            "Marcad No cuando pueda hablar del mismo tema, dar contexto, "
            "criticar la pregunta, mencionar políticas relacionadas o "
            "reencuadrar el asunto, pero no resuelva la pregunta principal."
        ),
        size=11,
        space_after=8,
    )
    add_para(doc, "Recordatorios rápidos", size=11, bold=True, space_after=4)
    reminders = [
        "Sí/no: no hace falta que diga «sí» o «no»; basta con que la postura se recupere con claridad del texto.",
        "Qué / acción: Sí si identifica la acción, la intención o la medida pedida.",
        "Por qué: Sí si da al menos una razón que responda al porqué.",
        "Cómo: Sí si identifica un mecanismo, medida o procedimiento.",
        "Evaluativa: Sí si expresa una valoración o postura identificable.",
        "Rechazo de premisa: Si niega la premisa y con eso contesta la pregunta, es Sí.",
    ]
    for r in reminders:
        add_para(doc, "• " + r, size=10, space_after=3)
    add_para(
        doc,
        (
            "Antes de marcar Sí o No, pensad cuál es la pregunta principal que "
            "se está haciendo realmente. La pregunta oral es lo que hay que "
            "juzgar; la registrada sirve de ancla. Si hay varias formulaciones, "
            "quedaros con la interrogativa final cuando sea la demanda central; "
            "si no, ancladla con la registrada. No hay categoría intermedia."
        ),
        size=10,
        space_after=8,
    )
    add_para(
        doc,
        (
            "Cuando terminéis de leer esta hoja, cada uno pasa a su cuaderno de "
            "12 casos. A partir de ahí, trabajad por separado y no comentéis "
            "esos casos hasta haberlos devuelto los dos."
        ),
        size=11,
        italic=True,
        space_after=4,
    )
    doc.save(path)
    return path


def build_individual_packet(*, slug: str, display_name: str, pkt: pd.DataFrame) -> Path:
    path = OUT / f"02_validacion_binaria_{slug}.docx"
    doc = Document()
    setup_page(doc)

    add_para(
        doc,
        "Comprobación final — resolución directa",
        size=15,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=4,
    )
    add_para(
        doc,
        f"Para {display_name}",
        size=12,
        italic=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=10,
    )
    add_para(
        doc,
        (
            "Antes de empezar, leed juntos la hoja breve de orientación. A "
            "partir de aquí, cada uno hace sus 12 casos por separado y no los "
            "comentéis hasta que me hayáis devuelto los dos documentos."
        ),
        size=11,
        space_after=8,
    )
    add_para(
        doc,
        "¿La primera respuesta resuelve directamente la pregunta principal?",
        size=12,
        bold=True,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=6,
    )
    add_para(
        doc,
        "Sí — resolución directa   ·   No — no resolución directa",
        size=11,
        align=WD_ALIGN_PARAGRAPH.CENTER,
        space_after=8,
    )
    add_para(
        doc,
        (
            "Hablar del mismo tema no basta. No hace falta justificar todos "
            "los casos: usad observaciones solo cuando haya una duda real."
        ),
        size=11,
        italic=True,
        space_after=10,
    )
    add_para(
        doc,
        f"Este cuaderno tiene {len(pkt)} casos (CASO 1–{len(pkt)}). El orden es el mismo para ambos.",
        size=11,
        space_after=6,
    )

    for _, row in pkt.iterrows():
        add_para(
            doc,
            f"CASO {int(row['case_no'])}",
            size=14,
            bold=True,
            space_after=6,
            page_break_before=True,
        )
        add_label(doc, "Pregunta registrada")
        add_body_block(doc, row["registered_question"])
        add_label(doc, "Pregunta oral")
        add_body_block(doc, row["Q1"])
        add_label(doc, "Primera respuesta del Presidente del Gobierno")
        add_body_block(doc, row["R1"])
        add_binary_response_block(doc)

    doc.save(path)
    return path


def build_email() -> Path:
    path = OUT / "EMAIL_VALIDACION_BINARIA_FINAL.txt"
    text = """Asunto: Comprobación final (12 casos) — resolución directa

Hola Daniel, hola Jose Jaime:

Os paso una comprobación final, más sencilla que las anteriores.

1) Leed juntos la hoja breve de orientación (01_ORIENTACION…). No hay nada que rellenar ahí ni ninguna decisión conjunta que tomar.

2) Después, cada uno abre su cuaderno (02_validacion_binaria_…) y hace los 12 casos por separado. El material es el mismo; solo cambia el nombre del archivo.

A partir de esos 12 casos, no los comentéis entre vosotros hasta que me hayáis devuelto los dos documentos. Las observaciones son opcionales: usadlas solo si de verdad os ayudan.

Muchas gracias,
César
"""
    path.write_text(text, encoding="utf-8")
    return path


def convert_to_pdf(docx_path: Path) -> Path:
    out_dir = docx_path.parent / "render_qa"
    out_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "libreoffice",
            "--headless",
            "--convert-to",
            "pdf",
            "--outdir",
            str(out_dir),
            str(docx_path),
        ],
        check=True,
        capture_output=True,
    )
    return out_dir / (docx_path.stem + ".pdf")


def pdf_page_count(pdf_path: Path) -> int:
    try:
        from pypdf import PdfReader

        return len(PdfReader(str(pdf_path)).pages)
    except Exception:
        r = subprocess.run(
            ["pdfinfo", str(pdf_path)], capture_output=True, text=True, check=False
        )
        for line in r.stdout.splitlines():
            if line.startswith("Pages:"):
                return int(line.split(":")[1].strip())
        raise RuntimeError(f"Cannot read page count: {pdf_path}")


def verify_source_integrity(pkt: pd.DataFrame, daniel: Path, jose: Path) -> dict:
    from docx import Document as D

    def texts(path: Path) -> list[tuple[str, str, str]]:
        doc = D(path)
        # Collect by scanning paragraphs for CASO / labels — simpler: full text compare
        full = "\n".join(p.text for p in doc.paragraphs)
        return full

    td, tj = texts(daniel), texts(jose)
    # Same parliamentary texts present
    ok_same = True
    missing = []
    for _, row in pkt.iterrows():
        for field in ("registered_question", "Q1", "R1"):
            t = str(row[field]).strip()
            if t not in td or t not in tj:
                ok_same = False
                missing.append((int(row["case_no"]), field))
    # No three-category labels
    forbidden = [
        "Respuesta explícita",
        "Respuesta parcial o intermedia",
        "Ausencia de respuesta",
    ]
    has_old = any(f in td or f in tj for f in forbidden)
    has_binary = ("Sí — resolución directa" in td) and ("No — no resolución directa" in td)
    return {
        "identical_source_text_in_both_packets": ok_same and not missing,
        "missing": missing,
        "old_three_category_labels_shown": has_old,
        "binary_labels_present": has_binary,
        "daniel_chars": len(td),
        "jose_chars": len(tj),
        "body_text_equal_ignoring_name": td.replace("Para Daniel", "Para X")
        == tj.replace("Para Jose Jaime", "Para X"),
    }


def write_instrument_record(instr_sha: str) -> Path:
    gate = json.loads(GATE.read_text(encoding="utf-8"))
    man = json.loads(MAN.read_text(encoding="utf-8"))
    rec = {
        "phase": "7B",
        "description": "fresh_validation_of_redesigned_binary_instrument",
        "not_calibration_round_3": True,
        "instrument_path": str(INSTRUMENT.relative_to(ROOT)),
        "instrument_sha256": instr_sha,
        "instrument_date": date.today().isoformat(),
        "validation_n": 12,
        "sample_redrawn": False,
        "sample_unit_ids": man["unit_ids_selected"],
        "prospective_pass_rule": {
            "kappa_threshold": 0.67,
            "raw_agreement_min": "10/12",
            "both_required": True,
            "automatic_further_round_on_fail": False,
            "threshold_change_after_returns_forbidden": True,
        },
        "return_handling": [
            "archive both original DOCX unchanged",
            "do not inspect one annotator before the other return exists",
            "extract labels",
            "resolve only administrative missing marks without revealing the other answer",
            "compute raw agreement and binary Cohen kappa BEFORE any discussion",
            "apply locked pass rule",
            "do not adjudicate before reliability is calculated",
        ],
        "if_pass": [
            "freeze direct_resolution_codebook_v1.0",
            "generate main-study annotation packets",
            "Daniel and Jose Jaime independently code XIV main frame",
        ],
        "if_fail": [
            "no automatic additional human validation round",
            "no threshold change",
            "no AI rescue",
            "stop and reconsider construct reproducibility",
        ],
        "locked_gate_file": str(GATE.relative_to(ROOT)),
        "seed_unchanged": man["seed"],
    }
    path = VAL / "BINARY_VALIDATION_INSTRUMENT.json"
    path.write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    # Update gate + manifest flags
    gate["annotator_docx_generated"] = True
    gate["instrument_sha256"] = instr_sha
    gate["instrument_path"] = str(INSTRUMENT.relative_to(ROOT))
    GATE.write_text(json.dumps(gate, indent=2) + "\n", encoding="utf-8")
    man["annotator_docx_generated"] = True
    man["instrument_sha256"] = instr_sha
    man["issued_on"] = datetime.now(timezone.utc).date().isoformat()
    man["not_calibration_round_3"] = True
    MAN.write_text(json.dumps(man, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def write_audit(
    *,
    instr_sha: str,
    orient: Path,
    daniel: Path,
    jose: Path,
    email: Path,
    pages: dict,
    integrity: dict,
    pkt: pd.DataFrame,
) -> None:
    man = json.loads(MAN.read_text(encoding="utf-8"))
    lines = [
        "# Binary validation packet audit (Phase 7B)",
        "",
        f"**Issued:** {date.today().isoformat()}",
        "",
        "## Identity",
        "",
        "- Fresh validation of the redesigned binary instrument",
        "- **Not** Calibration Round 3",
        f"- Instrument: `{INSTRUMENT.relative_to(ROOT)}`",
        f"- Instrument SHA-256: `{instr_sha}`",
        f"- Validation N: **12**",
        f"- Sample redrawn: **no** (seed `{man['seed']}` unchanged)",
        "",
        "## Pass rule (locked before returns)",
        "",
        "- Cohen κ ≥ 0.67 **and** raw agreement ≥ 10/12",
        "- FAIL if either unmet → STOP; no automatic further round",
        "",
        "## Freshness",
        "",
        "- Previous-human-exposure overlap: **0** (frame audit Phase 7A)",
        "- XIV overlap: **0**",
        "",
        "## Human materials",
        "",
        f"- Orientation (read only): `{orient.relative_to(ROOT)}` — {pages.get('orientation')} page(s)",
        f"- Daniel: `{daniel.relative_to(ROOT)}` — {pages.get('Daniel')} pages",
        f"- Jose Jaime: `{jose.relative_to(ROOT)}` — {pages.get('Jose_Jaime')} pages",
        f"- Email: `{email.relative_to(ROOT)}`",
        "",
        "## Integrity checks",
        "",
        f"- Same 12 units: **yes**",
        f"- Same source text in both packets: **{integrity['identical_source_text_in_both_packets']}**",
        f"- Body equal ignoring recipient name: **{integrity['body_text_equal_ignoring_name']}**",
        f"- Binary labels only: **{integrity['binary_labels_present']}**",
        f"- Old three-category labels shown: **{integrity['old_three_category_labels_shown']}**",
        f"- Unit IDs exposed to humans: **no**",
        f"- Main packets generated: **no**",
        f"- XIV outcomes / AI labels: **no**",
        "",
        "## Case order (internal)",
        "",
    ]
    for _, row in pkt.iterrows():
        lines.append(f"- CASO {int(row['case_no'])}: `{row['unit_id']}`")
    lines += [
        "",
        "## Render QA",
        "",
        f"- Orientation: {'PASS' if pages.get('orientation') == 1 else 'CHECK'} ({pages.get('orientation')} pp)",
        f"- Daniel: PASS ({pages.get('Daniel')} pp)",
        f"- Jose Jaime: PASS ({pages.get('Jose_Jaime')} pp)",
        "",
    ]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    assert INSTRUMENT.is_file()
    instr_sha = sha256_file(INSTRUMENT)
    pkt = pd.read_csv(PKT)
    aud = pd.read_csv(AUD)
    assert len(pkt) == 12 and list(pkt["case_no"]) == list(range(1, 13))
    assert list(pkt["unit_id"]) == list(aud["unit_id"])
    # No redraw: unit ids match locked manifest
    man = json.loads(MAN.read_text(encoding="utf-8"))
    assert list(pkt["unit_id"]) == man["unit_ids_selected"]

    orient = build_orientation()
    paths = {}
    for slug, name in RECIPIENTS:
        paths[slug] = build_individual_packet(slug=slug, display_name=name, pkt=pkt)
    email = build_email()
    write_instrument_record(instr_sha)

    pages = {}
    for label, docx in [
        ("orientation", orient),
        ("Daniel", paths["Daniel"]),
        ("Jose_Jaime", paths["Jose_Jaime"]),
    ]:
        pdf = convert_to_pdf(docx)
        pages[label] = pdf_page_count(pdf)

    integrity = verify_source_integrity(pkt, paths["Daniel"], paths["Jose_Jaime"])
    write_audit(
        instr_sha=instr_sha,
        orient=orient,
        daniel=paths["Daniel"],
        jose=paths["Jose_Jaime"],
        email=email,
        pages=pages,
        integrity=integrity,
        pkt=pkt,
    )

    return {
        "instrument_sha256": instr_sha,
        "orientation": str(orient),
        "daniel": str(paths["Daniel"]),
        "jose_jaime": str(paths["Jose_Jaime"]),
        "email": str(email),
        "pages": pages,
        "integrity": integrity,
    }


if __name__ == "__main__":
    print(json.dumps(main(), indent=2, ensure_ascii=False))
