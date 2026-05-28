"""Tests for MCP client setup."""

import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from src.client import MCP_URL, financial_mcp_session


def test_mcp_url_points_to_api_endpoint():
    assert MCP_URL == "https://mcp.financialdatasets.ai/api"


@pytest.mark.asyncio
async def test_missing_api_key_raises():
    with patch.dict(os.environ, {}, clear=True):
        os.environ.pop("FINANCIAL_DATASETS_API_KEY", None)
        with pytest.raises(EnvironmentError, match="FINANCIAL_DATASETS_API_KEY"):
            async with financial_mcp_session():
                pass


@pytest.mark.asyncio
async def test_session_passes_api_key_header():
    """Client must inject X-API-KEY header when opening the streamable-http connection."""
    mock_session = AsyncMock()
    mock_session.initialize = AsyncMock()

    fake_streams = (AsyncMock(), AsyncMock(), None)

    with patch.dict(os.environ, {"FINANCIAL_DATASETS_API_KEY": "test-key-123"}):
        with patch("src.client.streamablehttp_client") as mock_transport:
            mock_transport.return_value.__aenter__ = AsyncMock(return_value=fake_streams)
            mock_transport.return_value.__aexit__ = AsyncMock(return_value=False)
            with patch("src.client.ClientSession") as mock_cls:
                mock_cls.return_value.__aenter__ = AsyncMock(return_value=mock_session)
                mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

                async with financial_mcp_session() as session:
                    assert session is mock_session

                mock_transport.assert_called_once_with(
                    MCP_URL,
                    headers={"X-API-KEY": "test-key-123"},
                )
                mock_session.initialize.assert_awaited_once()
