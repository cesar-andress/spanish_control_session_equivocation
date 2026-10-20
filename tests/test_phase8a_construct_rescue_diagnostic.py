"""Phase 8A diagnostic present; binary FAIL preserved; no v1.0 / XIV outcomes."""

from __future__ import annotations

import json
from pathlib import Path

from scse.paths import DATA_PRIVATE, PROJECT_ROOT, PROTOCOL_DIR

REP = PROJECT_ROOT / "_internal" / "reports"


def test_diagnostic_and_binary_fail_preserved():
    diag = (REP / "FINAL_CONSTRUCT_RESCUE_DIAGNOSTIC.md").read_text(encoding="utf-8")
    assert "LIKELY YES" in diag or "LIKELY NO" in diag
    assert "requested response component" in diag.lower() or "requested_feature" in diag
    agr = json.loads((REP / "BINARY_VALIDATION_AGREEMENT.json").read_text())
    assert agr["locked_gate_decision"]["gate"] == "FAIL"
    assert not (PROTOCOL_DIR / "direct_resolution_codebook_v1.0.md").is_file()
    pool = DATA_PRIVATE / "eligible_pool_full.parquet"
    if pool.is_file():
        import pandas as pd
        df = pd.read_parquet(pool)
        assert "direct_resolution" not in df.columns
