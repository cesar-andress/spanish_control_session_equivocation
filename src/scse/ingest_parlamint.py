"""Acquire and verify pinned ParlaMint-ES 5.0 archive."""

from __future__ import annotations

import hashlib
import json
import shutil
import tarfile
from datetime import datetime, timezone
from pathlib import Path

from scse.config import (
    PARLAMINT_ARCHIVE,
    PARLAMINT_HANDLE,
    PARLAMINT_MD5,
    PARLAMINT_RELEASE,
    PARLAMINT_SHA256,
)
from scse.paths import MANIFESTS_DIR, PARLAMINT_CACHE, RAW_PINNED_DIR, ensure_private_layout

# Authoritative CLARIN.SI distribution page (handle resolves here)
PARLAMINT_SOURCE_PAGE = "https://www.clarin.si/repository/xmlui/handle/11356/2004"


def _sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _md5(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def locate_existing_archive() -> Path | None:
    """Reuse a locally verified sibling SPDB copy when present (same MD5 as CLARIN 5.0)."""
    from scse.paths import PROJECT_ROOT

    candidates = [
        PROJECT_ROOT.parent
        / "p01_spanish_political_discourse_benchmark"
        / "spanish_political_discourse_benchmark"
        / "data"
        / "raw"
        / "parlamint"
        / "ParlaMint-ES.tgz",
        PARLAMINT_CACHE / PARLAMINT_ARCHIVE,
    ]
    for cand in candidates:
        if cand.is_file() and _md5(cand) == PARLAMINT_MD5:
            return cand
    return None


def ensure_parlamint_archive() -> dict:
    ensure_private_layout()
    dest = PARLAMINT_CACHE / PARLAMINT_ARCHIVE
    existing = locate_existing_archive()
    if existing is None:
        raise FileNotFoundError(
            "ParlaMint-ES.tgz with expected MD5 not found locally. "
            f"Download from {PARLAMINT_SOURCE_PAGE} into {PARLAMINT_CACHE}."
        )
    if not dest.exists() or dest.resolve() != existing.resolve():
        if dest.exists() and _md5(dest) != PARLAMINT_MD5:
            raise RuntimeError(f"Refusing to overwrite mismatched archive at {dest}")
        if not dest.exists():
            try:
                dest.hardlink_to(existing)
            except OSError:
                shutil.copy2(existing, dest)

    sha = _sha256(dest)
    md5 = _md5(dest)
    if md5 != PARLAMINT_MD5:
        raise RuntimeError(f"MD5 mismatch: got {md5}, expected {PARLAMINT_MD5}")
    if sha != PARLAMINT_SHA256:
        raise RuntimeError(f"SHA-256 mismatch: got {sha}, expected {PARLAMINT_SHA256}")

    tei_dir = PARLAMINT_CACHE / "ParlaMint-ES.TEI"
    if not tei_dir.is_dir():
        with tarfile.open(dest, "r:gz") as tar:
            tar.extractall(path=PARLAMINT_CACHE)

    # Public-intent pointer (checksums only; no bulk TEI under zenodo/)
    RAW_PINNED_DIR.mkdir(parents=True, exist_ok=True)
    pointer = {
        "source": "ParlaMint-ES",
        "release": PARLAMINT_RELEASE,
        "handle": PARLAMINT_HANDLE,
        "source_page": PARLAMINT_SOURCE_PAGE,
        "archive": PARLAMINT_ARCHIVE,
        "sha256": sha,
        "md5": md5,
        "bytes": dest.stat().st_size,
        "cache_relpath": "_internal/source_cache/parlamint/ParlaMint-ES.tgz",
        "licence": "CC BY 4.0",
        "note": "Bulk archive stored in private source cache; not committed.",
    }
    (RAW_PINNED_DIR / "parlamint_es_5.0.json").write_text(
        json.dumps(pointer, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return pointer


def write_acquisition_manifest(entries: list[dict]) -> Path:
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    path = MANIFESTS_DIR / "source_acquisition.json"
    payload = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "sources": entries,
    }
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def main() -> int:
    pointer = ensure_parlamint_archive()
    write_acquisition_manifest(
        [
            {
                "source": pointer["source"],
                "version": pointer["release"],
                "URL": pointer["handle"],
                "retrieved_at": datetime.now(timezone.utc).isoformat(),
                "filename": pointer["archive"],
                "sha256": pointer["sha256"],
                "licence_status": "CC-BY-4.0",
                "coverage": "2015-01-20 to 2023-02-23 (observed in archive)",
                "notes": "Verified against CLARIN.SI published MD5 for ParlaMint 5.0",
            }
        ]
    )
    print(json.dumps(pointer, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
