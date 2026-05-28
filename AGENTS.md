# AGENTS.md — financial-data-mcp

## Setup

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env  # then add your FINANCIAL_DATASETS_API_KEY
```

## Running

```bash
pytest                   # all unit tests
pytest -m integration    # live MCP tests (requires real API key)
ruff check .             # lint
financial-agent AAPL     # demo CLI
```

## Code Style

- Python 3.11+; use `X | Y` union syntax, not `Optional[X]`
- `async`/`await` throughout — no sync wrappers around async code
- `const` style: prefer module-level constants for URLs and defaults
- Named exports from `src/tools.py` — no `import *`
- Early returns to reduce nesting
- Type-annotate all function signatures

## Testing Instructions

**Always write tests before implementing (red/green TDD):**

1. Write a failing test in `tests/`
2. Run `pytest` — confirm it fails (red)
3. Implement the feature
4. Run `pytest` — confirm it passes (green)
5. Run `ruff check .`

**Test conventions:**
- Use `AsyncMock` for session + tool mocks
- Assert on `session.call_tool.call_args` to verify tool name and params
- Name tests: `test_<what>_<when_condition>` (e.g., `test_get_news_without_ticker_omits_ticker_param`)
- Integration tests: mark with `@pytest.mark.integration`, skip in CI

## PR Instructions

- Every PR must include evidence you tested it (pytest output or manual test notes)
- Review AI-generated PR descriptions before merging — they can be wrong
- Keep PRs focused: one feature or fix per PR
- Never remove or weaken existing tests
- Reference the relevant `TODO.md` item in the PR description
