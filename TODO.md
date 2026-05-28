# financial-data-mcp — Task Breakdown

## How to Use This File

Per task:
1. Write tests FIRST (red — confirm they fail before implementing)
2. Implement until tests pass (green)
3. Review diff manually
4. Commit with descriptive message
5. Update CLAUDE.md / AGENTS.md if you learned something new

---

## Phase 0: Foundation ✅
- [x] `pyproject.toml` with mcp, pytest-asyncio, ruff
- [x] `src/client.py` — MCP session factory
- [x] `src/tools.py` — typed tool wrappers
- [x] `src/agent.py` — demo CLI entry point
- [x] `tests/test_client.py` — client auth & header tests
- [x] `tests/test_tools.py` — tool wrapper unit tests
- [x] GitHub Actions CI (`pytest` + `ruff check`)
- [ ] Install deps and confirm `pytest` green locally
- [ ] Review AI config files (CLAUDE.md, AGENTS.md, copilot-instructions.md)

## Phase 1: Full Tool Coverage ⬜
- [ ] Add wrappers for remaining tools: `get_filings`, `get_filing_items`, `list_filing_item_types`
- [ ] Add wrappers for: `get_segmented_financials`, `get_institutional_holdings`, `get_institutional_investors`
- [ ] Add wrappers for: `get_kpi_metrics`, `get_kpi_guidance`, `get_kpi_non_gaap`
- [ ] Write tests for each new wrapper (red → green)
- [ ] `list_stock_screener_filters` wrapper + test

## Phase 2: Agent Intelligence ⬜
- [ ] Build a simple REPL / interactive agent loop in `src/agent.py`
- [ ] Add natural-language → tool routing (map questions to MCP tool calls)
- [ ] Multi-ticker comparison helper (e.g., compare P/E ratios across a list)
- [ ] Portfolio snapshot: given a list of tickers, return price + metrics for all
- [ ] Tests for routing logic (mock session)

## Phase 3: Usability & Output ⬜
- [ ] Pretty-print / table formatting for CLI output (rich or tabulate)
- [ ] JSON and CSV export options for data results
- [ ] Configurable output verbosity (`--quiet`, `--json`)
- [ ] Error handling: rate limits, 401, 402 (subscription required) — user-friendly messages
- [ ] Integration test against live MCP server (requires real API key, skipped in CI)

## Phase 4: Ship ⬜
- [ ] `docs/spec.md` final review — mark implemented features
- [ ] Update README with demo GIF or sample output
- [ ] Semantic version tag `v0.1.0`
- [ ] GitHub release with changelog

---

## Parking Lot 🅿️
- Webhook receiver for real-time earnings / price events
- LangChain or Claude tool-use adapter layer
- MCP OAuth flow for interactive (non-API-key) usage

## Lessons Learned 📝
<!-- Add discoveries here as you work — they compound! -->
