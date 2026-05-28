# financial-data-mcp

> AI agent that queries real-time and historical financial data via the Financial Datasets MCP server

[![CI](https://github.com/ujjwalj/financial-data-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/ujjwalj/financial-data-mcp/actions/workflows/ci.yml)
🚧 **Early Development**

## What it does

Connects to the [Financial Datasets](https://financialdatasets.ai) remote MCP server (`https://mcp.financialdatasets.ai/api`) and exposes typed Python wrappers for all 25+ tools — stock prices, financial statements, SEC filings, earnings, news, insider trades, institutional holdings, macro rates, and stock screening.

## Tech Stack

- **Python 3.11+** — async/await throughout
- **mcp SDK** — `streamablehttp_client` + `ClientSession`
- **pytest + pytest-asyncio** — async test suite
- **ruff** — linting & formatting
- **hatch** — build backend

## Getting Started

```bash
# 1. Clone
git clone https://github.com/ujjwalj/financial-data-mcp.git
cd financial-data-mcp

# 2. Install (in a virtual env)
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# 3. Set your API key (get one at financialdatasets.ai)
cp .env.example .env
# edit .env — set FINANCIAL_DATASETS_API_KEY

# 4. Run tests
pytest

# 5. Run demo
export FINANCIAL_DATASETS_API_KEY=<your-key>
financial-agent AAPL
```

## Project Structure

```
financial-data-mcp/
├── src/
│   ├── client.py     # MCP session factory (auth, connection)
│   ├── tools.py      # Typed wrappers for all 25+ MCP tools
│   └── agent.py      # Demo agent / CLI entry point
├── tests/
│   ├── test_client.py
│   └── test_tools.py
├── docs/
│   ├── spec.md       # Feature spec
│   └── adr/          # Architecture decision records
├── .github/
│   └── workflows/ci.yml
├── pyproject.toml
├── .env.example
├── CLAUDE.md
├── AGENTS.md
└── TODO.md
```

## Available MCP Tools

| Category | Tools |
|---|---|
| Stock Prices | `get_stock_price`, `get_stock_prices` |
| Financials | `get_income_statement`, `get_balance_sheet`, `get_cash_flow_statement` |
| Metrics | `get_financial_metrics`, `get_financial_metrics_snapshot` |
| Company | `get_company_facts` |
| Earnings | `get_earnings` |
| News | `get_news` |
| SEC Filings | `get_filings`, `get_filing_items`, `list_filing_item_types` |
| Insider Trades | `get_insider_trades` |
| Institutional | `get_institutional_holdings`, `get_institutional_investors` |
| KPIs | `get_kpi_metrics`, `get_kpi_guidance`, `get_kpi_non_gaap` |
| Screener | `screen_stocks`, `list_stock_screener_filters` |
| Macro | `get_interest_rates` |
| Segmented | `get_segmented_financials` |

## Contributing

- Write tests **first** (red phase), then implement (green phase)
- Every PR must include evidence it was tested (test output or manual test notes)
- Keep PRs small and focused — one feature or fix per PR
- Review AI-generated PR descriptions before merging — they can be wrong
