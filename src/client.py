"""MCP client factory for Financial Datasets."""

import os
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

MCP_URL = "https://mcp.financialdatasets.ai/api"


@asynccontextmanager
async def financial_mcp_session() -> AsyncGenerator[ClientSession, None]:
    """Open an authenticated MCP session to Financial Datasets."""
    api_key = os.environ.get("FINANCIAL_DATASETS_API_KEY")
    if not api_key:
        raise EnvironmentError("FINANCIAL_DATASETS_API_KEY env var is not set")

    async with streamablehttp_client(
        MCP_URL,
        headers={"X-API-KEY": api_key},
    ) as streams:
        read_stream, write_stream, _ = streams
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            yield session
