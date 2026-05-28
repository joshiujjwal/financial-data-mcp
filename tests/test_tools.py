"""Tests for MCP tool wrappers."""

from unittest.mock import AsyncMock, MagicMock

import pytest

from src.tools import (
    get_balance_sheet,
    get_cash_flow_statement,
    get_company_facts,
    get_earnings,
    get_financial_metrics,
    get_financial_metrics_snapshot,
    get_income_statement,
    get_insider_trades,
    get_interest_rates,
    get_news,
    get_stock_price,
    get_stock_prices,
    list_available_tools,
    screen_stocks,
)


def make_session(return_value=None):
    session = AsyncMock()
    result = MagicMock()
    result.content = return_value or {"data": "mock"}
    session.call_tool = AsyncMock(return_value=result)
    return session


@pytest.mark.asyncio
async def test_get_stock_price_calls_correct_tool():
    session = make_session({"price": 195.5})
    result = await get_stock_price(session, "AAPL")
    session.call_tool.assert_awaited_once_with("get_stock_price", {"ticker": "AAPL"})
    assert result == {"price": 195.5}


@pytest.mark.asyncio
async def test_get_stock_prices_passes_all_params():
    session = make_session()
    await get_stock_prices(session, "TSLA", "2024-01-01", "2024-06-01", interval="week")
    session.call_tool.assert_awaited_once_with(
        "get_stock_prices",
        {"ticker": "TSLA", "start_date": "2024-01-01", "end_date": "2024-06-01", "interval": "week"},
    )


@pytest.mark.asyncio
async def test_get_stock_prices_default_interval():
    session = make_session()
    await get_stock_prices(session, "MSFT", "2024-01-01", "2024-03-01")
    call_args = session.call_tool.call_args[0][1]
    assert call_args["interval"] == "day"


@pytest.mark.asyncio
async def test_get_income_statement_defaults():
    session = make_session()
    await get_income_statement(session, "AAPL")
    call_args = session.call_tool.call_args[0][1]
    assert call_args["period"] == "quarterly"
    assert call_args["limit"] == 4


@pytest.mark.asyncio
async def test_get_news_without_ticker_omits_ticker_param():
    session = make_session()
    await get_news(session, limit=5)
    call_args = session.call_tool.call_args[0][1]
    assert "ticker" not in call_args
    assert call_args["limit"] == 5


@pytest.mark.asyncio
async def test_get_news_with_ticker_includes_it():
    session = make_session()
    await get_news(session, ticker="NVDA", limit=3)
    call_args = session.call_tool.call_args[0][1]
    assert call_args["ticker"] == "NVDA"


@pytest.mark.asyncio
async def test_get_earnings_without_ticker():
    session = make_session()
    await get_earnings(session)
    call_args = session.call_tool.call_args[0][1]
    assert "ticker" not in call_args


@pytest.mark.asyncio
async def test_get_earnings_with_ticker():
    session = make_session()
    await get_earnings(session, ticker="NFLX")
    call_args = session.call_tool.call_args[0][1]
    assert call_args["ticker"] == "NFLX"


@pytest.mark.asyncio
async def test_screen_stocks_passes_filters():
    session = make_session()
    filters = [{"field": "market_cap", "operator": "gte", "value": 1_000_000_000}]
    await screen_stocks(session, filters)
    session.call_tool.assert_awaited_once_with("screen_stocks", {"filters": filters})


@pytest.mark.asyncio
async def test_list_available_tools():
    session = AsyncMock()
    tool1 = MagicMock()
    tool1.name = "get_stock_price"
    tool2 = MagicMock()
    tool2.name = "get_news"
    tools_result = MagicMock()
    tools_result.tools = [tool1, tool2]
    session.list_tools = AsyncMock(return_value=tools_result)

    names = await list_available_tools(session)
    assert names == ["get_stock_price", "get_news"]


@pytest.mark.parametrize("fn,tool_name,kwargs", [
    (get_balance_sheet, "get_balance_sheet", {"ticker": "AAPL"}),
    (get_cash_flow_statement, "get_cash_flow_statement", {"ticker": "AAPL"}),
    (get_financial_metrics, "get_financial_metrics", {"ticker": "AAPL"}),
    (get_financial_metrics_snapshot, "get_financial_metrics_snapshot", {"ticker": "AAPL"}),
    (get_company_facts, "get_company_facts", {"ticker": "AAPL"}),
    (get_insider_trades, "get_insider_trades", {"ticker": "AAPL"}),
    (get_interest_rates, "get_interest_rates", {}),
])
@pytest.mark.asyncio
async def test_tool_wrappers_call_correct_mcp_tool(fn, tool_name, kwargs):
    session = make_session()
    await fn(session, **kwargs)
    actual_tool = session.call_tool.call_args[0][0]
    assert actual_tool == tool_name
