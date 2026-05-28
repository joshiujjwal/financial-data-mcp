# financial-data-mcp — Feature Specification

## Overview

A Python async client and agent that connects to the Financial Datasets remote MCP server, exposing typed wrappers for all available tools and a CLI entry point for querying real-time and historical market data.

**Problem:** Accessing 25+ financial data endpoints requires managing authentication, serialization, and error handling consistently across every call. This project provides a clean async Python interface so agents and scripts can focus on the data rather than the plumbing.

---

## Functional Requirements

### Authentication
- [x] Read `FINANCIAL_DATASETS_API_KEY` from environment
- [x] Inject key as `X-API-KEY` header via `streamablehttp_client`
- [ ] Friendly error when key is missing or invalid (401 / 402 responses)

### MCP Session Management
- [x] Context manager (`financial_mcp_session`) that opens, initializes, and closes the session
- [ ] Retry on transient network errors (max 3 attempts, exponential backoff)
- [ ] Timeout configurable via env var (`MCP_TIMEOUT_SECONDS`, default: 30)

### Tool Wrappers
All wrappers must:
- Accept typed parameters (no raw dicts from callers)
- Return the `result.content` value directly
- Have a corresponding unit test (mocked session)

| Tool | Status |
|---|---|
| `get_stock_price` | ✅ |
| `get_stock_prices` | ✅ |
| `get_income_statement` | ✅ |
| `get_balance_sheet` | ✅ |
| `get_cash_flow_statement` | ✅ |
| `get_financial_metrics` | ✅ |
| `get_financial_metrics_snapshot` | ✅ |
| `get_company_facts` | ✅ |
| `get_news` | ✅ |
| `get_insider_trades` | ✅ |
| `get_earnings` | ✅ |
| `screen_stocks` | ✅ |
| `get_interest_rates` | ✅ |
| `list_available_tools` | ✅ |
| `get_filings` | ⬜ |
| `get_filing_items` | ⬜ |
| `list_filing_item_types` | ⬜ |
| `get_segmented_financials` | ⬜ |
| `get_institutional_holdings` | ⬜ |
| `get_institutional_investors` | ⬜ |
| `get_kpi_metrics` | ⬜ |
| `get_kpi_guidance` | ⬜ |
| `get_kpi_non_gaap` | ⬜ |
| `list_stock_screener_filters` | ⬜ |

### CLI Agent (`src/agent.py`)
- [x] Demo mode: `financial-agent <TICKER>` prints price, metrics, facts, news
- [ ] Interactive REPL mode: ask questions, agent routes to correct MCP tools
- [ ] `--json` flag for machine-readable output
- [ ] `--compare TICKER1 TICKER2` for side-by-side metrics

---

## Non-Functional Requirements

- [ ] All tool calls complete within 10 seconds (enforced by session timeout)
- [ ] No secrets in source code — API key only via environment
- [ ] Python 3.11+ type hints throughout
- [ ] 100% unit test coverage of `src/tools.py` wrappers
- [ ] CI passes on every push (lint + tests)

---

## Data Model

Tool responses are returned as-is from `result.content` (the MCP SDK's parsed JSON). No additional mapping layer is applied in Phase 1 — callers receive the raw Financial Datasets response shape.

Future: typed Pydantic response models per tool.

---

## API / Interface Design

```python
# Open a session and call any tool
async with financial_mcp_session() as session:
    price = await get_stock_price(session, "AAPL")
    income = await get_income_statement(session, "AAPL", period="annual", limit=3)
    news   = await get_news(session, ticker="AAPL", limit=5)
```

---

## Test Plan

### Unit Tests (no network)
- Client: missing API key raises, correct header injected, `initialize()` called
- Tools: each wrapper calls correct MCP tool name with correct params
- Defaults: period="quarterly", limit=4, interval="day"
- Optional params: news without ticker omits `ticker` key, earnings without ticker sends empty dict

### Integration Tests (requires `FINANCIAL_DATASETS_API_KEY`)
- `get_stock_price("AAPL")` returns dict with price field
- `get_income_statement("MSFT")` returns list with at least 1 entry
- `screen_stocks([{market_cap ≥ 1B}])` returns non-empty list
- Mark with `@pytest.mark.integration` and skip in CI via `pytest -m "not integration"`

---

## Open Questions

1. Should tool wrappers return typed Pydantic models or raw dicts? (Phase 2 decision)
2. Should the REPL use Claude API / OpenAI for NL routing or a simple keyword matcher?
3. Webhook support for real-time events — out of scope for v0.1?
