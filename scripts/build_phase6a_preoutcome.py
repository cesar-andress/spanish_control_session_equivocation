"""Orchestrate Phase 6A pre-outcome main-study infrastructure."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from scse.analysis_scaffold import (  # noqa: E402
    category_distribution,
    confrontational_sensitivity,
    leave_one_questioner_out,
    make_synthetic_fixture,
    opposed_vs_nonopposed_contrast,
    per_questioner_explicit_rates,
    questioner_cluster_bootstrap,
)
from scse.main_frame import build_main_frame  # noqa: E402
from scse.main_packets import build_template_packets  # noqa: E402
from scse.main_source_review import build_source_review_pdf  # noqa: E402
from scse.preoutcome_assets import build_all_preoutcome_assets  # noqa: E402


def _smoke_analysis_synthetic() -> dict:
    syn = make_synthetic_fixture()
    return {
        "n_synthetic": len(syn),
        "dist": category_distribution(syn).to_dict(),
        "rd": opposed_vs_nonopposed_contrast(syn).risk_difference,
        "boot_lo_hi": (
            questioner_cluster_bootstrap(syn, n_boot=50, seed=0)["lo"],
            questioner_cluster_bootstrap(syn, n_boot=50, seed=0)["hi"],
        ),
        "loo_rows": len(leave_one_questioner_out(syn)),
        "per_q": len(per_questioner_explicit_rates(syn)),
        "confrontational_rows": len(confrontational_sensitivity(syn)),
    }


def main() -> int:
    frame = build_main_frame()
    review = build_source_review_pdf()
    packets = build_template_packets(issued=False)
    assets = build_all_preoutcome_assets()
    synthetic = _smoke_analysis_synthetic()
    out = {
        "phase": "6A",
        "main_frame_n": frame["n"],
        "completeness": frame["completeness"],
        "volumes": frame["volumes"]["recommended"],
        "source_review": review,
        "packets_issued": packets["issued"],
        "packet_templates": packets["paths"],
        "assets": assets,
        "synthetic_analysis_smoke": synthetic,
        "real_xiv_outcomes_used": False,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
