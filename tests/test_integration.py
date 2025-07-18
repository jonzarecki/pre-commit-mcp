import os
import sys
import asyncio
import pytest

from fastmcp import Client
from fastmcp.client.transports import FastMCPTransport
from fast_precommit_mcp import server

RESOURCE_URI = "resource://precommit-output"


@pytest.mark.asyncio
async def test_server_integration(tmp_path, monkeypatch):
    script = tmp_path / "pre-commit"
    script.write_text("#!/usr/bin/env python3\nprint('integrated')\n")
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")

    # Patch server helpers to avoid subprocess usage
    async def _noop_watch():
        return

    server._watch_changes = _noop_watch
    transport = FastMCPTransport(server.mcp)
    logs = []
    async with Client(transport, log_handler=lambda m: logs.append(m)) as client:
        out = await client.read_resource(RESOURCE_URI)
        assert out[0].text.strip() == "integrated"
        await client.call_tool("run_precommit_tool")
        out2 = await client.read_resource(RESOURCE_URI)
        assert out2[0].text.strip() == "integrated"
