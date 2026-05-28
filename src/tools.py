"""Typed wrappers around Financial Datasets MCP tools."""

from typing import Any

from mcp import ClientSession


async def get_stock_price(session: ClientSession, ticker: str) -> Any:
    result = await session.call_tool("get_stock_price", {"ticker": ticker})
    return result.content


async def get_stock_prices(
    session: ClientSession,
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
) -> Any:
    result = await session.call_tool(
        "get_stock_prices",
        {"ticker": ticker, "start_date": start_date, "end_date": end_date, "interval": interval},
    )
    return result.content


async def get_income_statement(
    session: ClientSession,
    ticker: str,
    period: str = "quarterly",
    limit: int = 4,
) -> Any:
    result = await session.call_tool(
        "get_income_statement",
        {"ticker": ticker, "period": period, "limit": limit},
    )
    return result.content


async def get_balance_sheet(
    session: ClientSession,
    ticker: str,
    period: str = "quarterly",
    limit: int = 4,
) -> Any:
    result = await session.call_tool(
        "get_balance_sheet",
        {"ticker": ticker, "period": period, "limit": limit},
    )
    return result.content


async def get_cash_flow_statement(
    session: ClientSession,
    ticker: str,
    period: str = "quarterly",
    limit: int = 4,
) -> Any:
    result = await session.call_tool(
        "get_cash_flow_statement",
        {"ticker": ticker, "period": period, "limit": limit},
    )
    return result.content


async def get_financial_metrics(
    session: ClientSession,
    ticker: str,
    period: str = "quarterly",
    limit: int = 4,
) -> Any:
    result = await session.call_tool(
        "get_financial_metrics",
        {"ticker": ticker, "period": period, "limit": limit},
    )
    return result.content


async def get_financial_metrics_snapshot(session: ClientSession, ticker: str) -> Any:
    result = await session.call_tool("get_financial_metrics_snapshot", {"ticker": ticker})
    return result.content


async def get_company_facts(session: ClientSession, ticker: str) -> Any:
    result = await session.call_tool("get_company_facts", {"ticker": ticker})
    return result.content


async def get_news(
    session: ClientSession,
    ticker: str | None = None,
    limit: int = 5,
) -> Any:
    params: dict[str, Any] = {"limit": limit}
    if ticker:
        params["ticker"] = ticker
    result = await session.call_tool("get_news", params)
    return result.content


async def get_insider_trades(
    session: ClientSession,
    ticker: str,
    limit: int = 10,
) -> Any:
    result = await session.call_tool("get_insider_trades", {"ticker": ticker, "limit": limit})
    return result.content


async def get_earnings(
    session: ClientSession,
    ticker: str | None = None,
) -> Any:
    params: dict[str, Any] = {}
    if ticker:
        params["ticker"] = ticker
    result = await session.call_tool("get_earnings", params)
    return result.content


async def screen_stocks(session: ClientSession, filters: list[dict[str, Any]]) -> Any:
    """Screen stocks using Financial Datasets filter syntax."""
    result = await session.call_tool("screen_stocks", {"filters": filters})
    return result.content


async def get_interest_rates(session: ClientSession) -> Any:
    result = await session.call_tool("get_interest_rates", {})
    return result.content


async def list_available_tools(session: ClientSession) -> list[str]:
    tools = await session.list_tools()
    return [t.name for t in tools.tools]
