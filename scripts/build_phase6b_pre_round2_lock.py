"""Phase 6B: restore Phase-0 probes, rebuild N=100 frame, orders, QA30 viewer."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from scse.main_frame import build_main_frame  # noqa: E402
from scse.main_packet_order import build_main_orderings  # noqa: E402
from scse.main_packets import build_template_packets  # noqa: E402
from scse.main_source_review import build_source_review_pdf  # noqa: E402
from scse.preoutcome_assets import build_all_preoutcome_assets  # noqa: E402
from scse.qa30_viewer import build_qa30_viewer  # noqa: E402


def main() -> int:
    frame = build_main_frame()
    orders = build_main_orderings()
    review = build_source_review_pdf()
    packets = build_template_packets(issued=False)
    assets = build_all_preoutcome_assets()
    qa_viewer = build_qa30_viewer()
    out = {
        "phase": "6B",
        "main_frame_n": frame["n"],
        "completeness": frame["completeness"],
        "volumes": frame["volumes"]["recommended"],
        "packet_orders": orders,
        "source_review": review,
        "packets_issued": packets["issued"],
        "assets": assets,
        "qa30_viewer": qa_viewer,
        "ai_simulation_run": False,
        "round2_returns_inspected": False,
        "xiv_reply_status_created": False,
    }
    print(json.dumps(out, indent=2, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
