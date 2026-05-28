# CLAUDE.md — financial-data-mcp

## Quick Start

```bash
pip install -e ".[dev]"           # install all deps
pytest                             # run test suite
ruff check .                       # lint
financial-agent AAPL               # run demo agent
```

## Required Environment

```bash
FINANCIAL_DATASETS_API_KEY=<key>  # from financialdatasets.ai/dashboard
```

Never hardcode keys. Load from `.env` in dev (use `python-dotenv` if you add it).

## Directory Map

| Path | Purpose |
|---|---|
| `src/client.py` | `financial_mcp_session()` — async context manager that opens an authenticated MCP connection |
| `src/tools.py` | Typed wrappers for every MCP tool; returns `result.content` directly |
| `src/agent.py` | CLI entry point and demo agent loop |
| `tests/` | Unit tests (all mocked — no live network calls) |
| `docs/spec.md` | Feature spec and tool coverage tracker |
| `docs/adr/` | Architecture Decision Records |
| `.github/workflows/ci.yml` | Runs `ruff check` + `pytest` on every push |

## Key Conventions

- **Async everywhere.** All MCP calls are `await`ed. Never use `asyncio.run()` inside a function — only at the top level of `agent.py`.
- **Session is the unit of work.** Open one `financial_mcp_session()` per logical operation. Don't leak sessions.
- **`result.content` is the return value.** MCP SDK returns a `CallToolResult`; always return `.content` from wrappers.
- **Optional params via `| None`.** Functions with optional MCP parameters should accept `None` and conditionally include keys in the params dict (see `get_news`, `get_earnings`).
- **Python 3.11+ syntax.** Use `X | Y` union types, `match` statements where appropriate.

## Workflow (follow this every session)

1. `pytest` — confirm baseline is green before touching anything
2. Check `TODO.md` for the next task
3. Write failing test (red)
4. Implement until test passes (green)
5. `ruff check .` — fix any lint issues
6. Review diff manually — don't ship unreviewed changes
7. `git commit` with a descriptive message
8. Update this file or `AGENTS.md` if you discovered something new

## MCP Server Details

- **URL:** `https://mcp.financialdatasets.ai/api` (API key auth)
- **Auth:** `X-API-KEY` header
- **Transport:** `streamablehttp_client` from `mcp.client.streamable_http`
- **Tools:** 25+ — see `docs/spec.md` for the full list and coverage status
- **Errors to handle:** 401 (bad key), 402 (subscription required for KPI tools), 404 (ticker not found)

## Gotchas

- `pytest-asyncio` requires `asyncio_mode = "auto"` (already set in `pyproject.toml`) — don't add `@pytest.mark.asyncio` manually, it's redundant but harmless
- `streamablehttp_client` returns a 3-tuple `(read, write, _)` — the third element is metadata, ignore it
- KPI tools (`get_kpi_*`) require a Pro/Enterprise subscription — expect 402 on free tier
- The MCP session must call `await session.initialize()` before any tool calls
