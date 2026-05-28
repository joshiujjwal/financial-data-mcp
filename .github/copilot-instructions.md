# GitHub Copilot Instructions — financial-data-mcp

## Stack

- Python 3.11+ with full async/await
- `mcp` SDK (`ClientSession`, `streamablehttp_client`)
- `pytest` + `pytest-asyncio` (asyncio_mode=auto)
- `ruff` for lint and format

## Coding Conventions

- Use `X | Y` union types, not `Optional[X]` or `Union[X, Y]`
- Prefer `async with` context managers — never leave MCP sessions open
- All tool wrappers in `src/tools.py` take `session: ClientSession` as first arg
- Return `result.content` from every tool wrapper — never the full `CallToolResult`
- Build params dicts conditionally (don't include `None` values as MCP params)
- Use early returns to reduce nesting

## Testing Conventions

- Mock `ClientSession` with `AsyncMock` — never make real network calls in unit tests
- Assert tool name via `session.call_tool.call_args[0][0]`
- Assert params via `session.call_tool.call_args[0][1]`
- Integration tests go in `tests/` marked with `@pytest.mark.integration`

## Boundaries

- Do not refactor existing code unless explicitly asked
- Do not remove or weaken existing tests
- Do not add new dependencies without discussion
- Do not hardcode `FINANCIAL_DATASETS_API_KEY` — always read from environment
- Do not create wrapper functions for tools not yet in `docs/spec.md`
