"""Example agent that uses the Financial Datasets MCP server."""

import asyncio

from .client import financial_mcp_session
from .tools import get_company_facts, get_financial_metrics_snapshot, get_news, get_stock_price


async def run_demo(ticker: str = "AAPL") -> None:
    async with financial_mcp_session() as session:
        print(f"=== Financial snapshot for {ticker} ===\n")

        price = await get_stock_price(session, ticker)
        print(f"[Price]\n{price}\n")

        metrics = await get_financial_metrics_snapshot(session, ticker)
        print(f"[Metrics]\n{metrics}\n")

        facts = await get_company_facts(session, ticker)
        print(f"[Company Facts]\n{facts}\n")

        news = await get_news(session, ticker=ticker, limit=3)
        print(f"[Latest News]\n{news}\n")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Financial Datasets MCP agent demo")
    parser.add_argument("ticker", nargs="?", default="AAPL", help="Stock ticker (default: AAPL)")
    args = parser.parse_args()
    asyncio.run(run_demo(args.ticker))


if __name__ == "__main__":
    main()
