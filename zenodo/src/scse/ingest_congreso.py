"""Acquire and parse Congreso initiative records for type 180/ oral questions."""

from __future__ import annotations

import hashlib
import json
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlencode
from urllib.request import Request, urlopen

from scse.config import CONGRESO_USER_AGENT, LEGISLATURE
from scse.paths import CONGRESO_CACHE, ensure_private_layout

CONGRESO_BASE = "https://www.congreso.es"
AVISO_LEGAL_URL = f"{CONGRESO_BASE}/es/cem/aviso-legal"
INICIATIVAS_SEARCH = f"{CONGRESO_BASE}/es/busqueda-de-iniciativas"
EXPEDIENTE_RE = re.compile(r"^180/\d{6}$")

# Documented reuse conditions (aviso legal, accessed 2026-09-29)
CONGRESO_REUSE_SUMMARY = (
    "Information on www.congreso.es is reusable provided the user: "
    "(a) does not alter the content; (b) does not distort its meaning; "
    "(c) cites the source; (d) mentions the date of last update; "
    "(e) uses content diligently / not unlawfully. "
    "Not expressed as a Creative Commons licence identifier."
)


@dataclass
class CongresoInitiative:
    expediente: str
    legislature: str
    title: str | None
    questioner_name: str | None
    parliamentary_group: str | None
    presented_date: str | None
    status: str | None
    ds_references: list[str]
    source_url: str
    retrieved_at: str
    html_sha256: str
    parse_notes: list[str]

    def to_dict(self) -> dict:
        return asdict(self)


def initiative_detail_url(expediente: str, legislature: str = LEGISLATURE) -> str:
    # expediente form 180/000128
    params = {
        "p_p_id": "iniciativas",
        "p_p_lifecycle": "0",
        "p_p_state": "normal",
        "p_p_mode": "view",
        "_iniciativas_mode": "mostrarDetalle",
        "_iniciativas_legislatura": legislature,
        "_iniciativas_id": expediente,
    }
    return f"{INICIATIVAS_SEARCH}?{urlencode(params, quote_via=quote)}"


def _cache_path(expediente: str, legislature: str) -> Path:
    safe = expediente.replace("/", "_")
    return CONGRESO_CACHE / "iniciativas" / f"{legislature}_{safe}.html"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def fetch_initiative_html(
    expediente: str,
    *,
    legislature: str = LEGISLATURE,
    sleep_s: float = 0.75,
    force: bool = False,
) -> tuple[Path, bytes, bool]:
    """Return (cache_path, html_bytes, from_cache). Never silently overwrite changed bytes.

    Raises FileNotFoundError when the Congreso portal returns a non-detail page
    (e.g. unknown expediente).
    """
    ensure_private_layout()
    path = _cache_path(expediente, legislature)
    if path.is_file() and not force:
        data = path.read_bytes()
        return path, data, True

    url = initiative_detail_url(expediente, legislature)
    req = Request(url, headers={"User-Agent": CONGRESO_USER_AGENT, "Accept": "text/html"})
    last_err: Exception | None = None
    data = b""
    for attempt in range(4):
        try:
            if attempt:
                time.sleep(min(8.0, sleep_s * (2**attempt)))
            with urlopen(req, timeout=60) as resp:
                data = resp.read()
            break
        except (HTTPError, URLError, TimeoutError) as exc:
            last_err = exc
    else:
        raise RuntimeError(f"Failed to fetch {expediente}: {last_err}")

    text = data.decode("utf-8", errors="replace")
    if "entradilla-iniciativa" not in text and 'name="description"' not in text:
        # Cache negative lookups lightly as empty marker? Prefer not to cache.
        raise FileNotFoundError(f"No initiative detail for {expediente}")

    if path.is_file():
        old = path.read_bytes()
        if old != data:
            raise RuntimeError(
                f"Upstream HTML changed for {expediente}; refusing silent overwrite. "
                f"old_sha={_sha256_bytes(old)} new_sha={_sha256_bytes(data)}"
            )
    else:
        path.write_bytes(data)
        time.sleep(sleep_s)
    return path, data, False


def parse_initiative_html(
    html: bytes | str,
    *,
    expediente: str,
    legislature: str,
    source_url: str,
) -> CongresoInitiative:
    if isinstance(html, bytes):
        raw = html
        text = html.decode("utf-8", errors="replace")
    else:
        raw = html.encode("utf-8")
        text = html
    notes: list[str] = []

    def meta(name: str) -> str | None:
        m = re.search(
            rf'<meta\s+content="([^"]*)"\s+name="{re.escape(name)}"',
            text,
            re.I,
        )
        if not m:
            m = re.search(
                rf'<meta\s+name="{re.escape(name)}"\s+content="([^"]*)"',
                text,
                re.I,
            )
        return m.group(1).strip() if m else None

    title = None
    m = re.search(
        r'class="entradilla-iniciativa"[^>]*>(.*?)</div>',
        text,
        re.I | re.S,
    )
    if m:
        title = re.sub(r"<[^>]+>", "", m.group(1))
        title = " ".join(title.split())
        # Strip trailing (180/######)
        title = re.sub(rf"\s*\({re.escape(expediente)}\)\s*$", "", title).strip()
    if not title:
        title = meta("description")
    if not title:
        notes.append("title_missing")

    questioner_name = None
    group = None
    # Author list item: Casado Blanco, Pablo (GP)
    m = re.search(
        r'busqueda-de-diputados[^"]*"[^>]*>([^<]+)\s*\(([^)]+)\)\s*</a>',
        text,
        re.I,
    )
    if m:
        questioner_name = " ".join(m.group(1).split())
        group = m.group(2).strip()
    else:
        kw = meta("keywords") or ""
        # "... ,  Pablo Casado Blanco"
        parts = [p.strip() for p in kw.split(",") if p.strip()]
        if parts:
            questioner_name = parts[-1]
            notes.append("questioner_from_keywords_meta")

    presented = None
    kw = meta("keywords") or ""
    m = re.search(r"Presentado el (\d{2}/\d{2}/\d{4})", kw)
    if m:
        d, mo, y = m.group(1).split("/")
        presented = f"{y}-{mo}-{d}"

    status = None
    m = re.search(r"Situaci[oó]n</[^>]+>\s*<[^>]+>([^<]+)", text, re.I)
    if m:
        status = " ".join(m.group(1).split())

    ds_refs: list[str] = []
    for dm in re.finditer(r"DSCD-\d+-PL-\d+", text):
        if dm.group(0) not in ds_refs:
            ds_refs.append(dm.group(0))
    # Also catch Diario patterns in custom HTML block
    m = re.search(r'id="_iniciativas_customHtmlDiarios"[^>]*>(.*?)</(?:div|script)', text, re.I | re.S)
    if m:
        block = re.sub(r"<[^>]+>", " ", m.group(1))
        for dm in re.finditer(r"DSCD-\d+-PL-\d+", block):
            if dm.group(0) not in ds_refs:
                ds_refs.append(dm.group(0))

    return CongresoInitiative(
        expediente=expediente,
        legislature=legislature,
        title=title,
        questioner_name=questioner_name,
        parliamentary_group=group,
        presented_date=presented,
        status=status,
        ds_references=ds_refs,
        source_url=source_url,
        retrieved_at=datetime.now(timezone.utc).isoformat(),
        html_sha256=_sha256_bytes(raw),
        parse_notes=notes,
    )


def acquire_initiatives(
    expedientes: list[str],
    *,
    legislature: str = LEGISLATURE,
    sleep_s: float = 0.75,
) -> list[CongresoInitiative]:
    ensure_private_layout()
    out: list[CongresoInitiative] = []
    catalog: list[dict] = []
    skipped: list[str] = []
    for exp in sorted(set(expedientes)):
        if not EXPEDIENTE_RE.fullmatch(exp):
            raise ValueError(f"Invalid expediente {exp!r}")
        try:
            path, data, from_cache = fetch_initiative_html(
                exp, legislature=legislature, sleep_s=sleep_s
            )
        except FileNotFoundError:
            skipped.append(exp)
            continue
        rec = parse_initiative_html(
            data,
            expediente=exp,
            legislature=legislature,
            source_url=initiative_detail_url(exp, legislature),
        )
        out.append(rec)
        catalog.append(
            {
                **rec.to_dict(),
                "cache_path": str(path.relative_to(CONGRESO_CACHE.parent.parent)),
                "from_cache": from_cache,
            }
        )
    catalog_path = CONGRESO_CACHE / "iniciativas_catalog.json"
    catalog_path.write_text(
        json.dumps(
            {"records": catalog, "skipped_missing": skipped},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    return out


def main() -> int:
    import sys

    exps = [a for a in sys.argv[1:] if EXPEDIENTE_RE.match(a)]
    if not exps:
        print("Usage: python -m scse.ingest_congreso 180/000128 [...]")
        return 2
    rows = acquire_initiatives(exps)
    for r in rows:
        print(r.expediente, r.title, r.questioner_name, r.parliamentary_group)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
