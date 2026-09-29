# Spanish control-session equivocation — public reproducibility Makefile
# Run from zenodo/

.DEFAULT_GOAL := help
SHELL := /bin/bash
.ONESHELL:

UV ?= uv
PYTEST ?= $(UV) run pytest
PYTHON ?= $(UV) run python

PHASE2_MSG := Phase 2 data acquisition has not yet been completed.
PHASE_LATER_MSG := This target depends on a later research phase that has not started.

.PHONY: help test data pool power calibrate freeze packets validate \
	agreement adjudicate analysis figures paper-assets release hygiene check-env

help: ## Show available targets
	@echo "Spanish control-session equivocation — Make targets"
	@echo ""
	@echo "  make test          Run unit and hygiene tests (available now)"
	@echo "  make hygiene       Scan public tree for private-path / secret patterns"
	@echo "  make check-env     Verify uv environment"
	@echo "  make data          Acquire pinned ParlaMint-ES + Congreso records (Phase 2)"
	@echo "  make pool          Extract eligible exchanges and hash pool (Phase 2)"
	@echo "  make power         Simulate CI half-widths for N decision (Phase 2)"
	@echo "  make calibrate     Draw calibration set and build packets (Phase 4)"
	@echo "  make freeze        Hash protocol/codebook; draw main sample (Phase 5)"
	@echo "  make packets       Build annotator XLSX packets (Phase 6)"
	@echo "  make validate      Schema-check returned packets (Phase 6)"
	@echo "  make agreement     Compute reliability metrics (Phase 7)"
	@echo "  make adjudicate    Build adjudication sheets / ingest log (Phase 7)"
	@echo "  make analysis      Pre-registered primary and secondary analyses (Phase 8)"
	@echo "  make figures       Generate figures F1–F2 (Phase 8)"
	@echo "  make paper-assets  Copy generated tables/figures into ../paper/ (Phase 8+)"
	@echo "  make release       Build release manifest and checksums (Phase 10)"
	@echo ""
	@echo "Targets other than test/help/hygiene/check-env fail safely until their phase."

check-env: ## Verify Python environment via uv
	@$(UV) --version
	@$(UV) run python -c "import sys; print(sys.version)"

test: ## Run pytest suite
	@$(PYTEST)

hygiene: ## Public-tree hygiene scan
	@$(PYTHON) scripts/hygiene_scan.py

data: ## Phase 2 stub
	@echo "$(PHASE2_MSG)"; exit 1

pool: ## Phase 2 stub
	@echo "$(PHASE2_MSG)"; exit 1

power: ## Phase 2 stub
	@echo "$(PHASE2_MSG)"; exit 1

calibrate: ## Phase 4 stub
	@echo "$(PHASE_LATER_MSG) (calibration)"; exit 1

freeze: ## Phase 5 stub
	@echo "$(PHASE_LATER_MSG) (protocol freeze)"; exit 1

packets: ## Phase 6 stub
	@echo "$(PHASE_LATER_MSG) (main annotation packets)"; exit 1

validate: ## Phase 6 stub
	@echo "$(PHASE_LATER_MSG) (packet validation)"; exit 1

agreement: ## Phase 7 stub
	@echo "$(PHASE_LATER_MSG) (reliability)"; exit 1

adjudicate: ## Phase 7 stub
	@echo "$(PHASE_LATER_MSG) (adjudication)"; exit 1

analysis: ## Phase 8 stub
	@echo "$(PHASE_LATER_MSG) (analysis)"; exit 1

figures: ## Phase 8 stub
	@echo "$(PHASE_LATER_MSG) (figures)"; exit 1

paper-assets: ## Phase 8+ stub
	@echo "$(PHASE_LATER_MSG) (paper assets)"; exit 1

release: ## Phase 10 stub
	@echo "$(PHASE_LATER_MSG) (public release packaging)"; exit 1
