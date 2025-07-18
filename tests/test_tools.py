import os
import sys
import asyncio
import pytest

from fast_precommit_mcp.tools import run_precommit
from fast_precommit_mcp import server


@pytest.mark.asyncio
async def test_run_precommit(tmp_path, monkeypatch):
    script = tmp_path / "pre-commit"
    script.write_text("#!/usr/bin/env python3\nprint('hook')\n")
    script.chmod(0o755)
    monkeypatch.setenv("PATH", f"{tmp_path}:{os.environ['PATH']}")
    lines = await run_precommit()
    assert lines == ["hook"]


class DummyCtx:
    def __init__(self):
        self.lines = []

    async def info(self, line):
        self.lines.append(line)


@pytest.mark.asyncio
async def test_run_precommit_stream(monkeypatch):
    async def fake_run_precommit(files=None):
        return ["a", "b"]

    monkeypatch.setattr(server, "run_precommit", fake_run_precommit)
    ctx = DummyCtx()
    await server._run_precommit_stream(ctx)
    assert server.LAST_OUTPUT == ["a", "b"]
    assert ctx.lines == ["a", "b"]


@pytest.mark.asyncio
async def test_precommit_output_resource():
    server.LAST_OUTPUT = ["x", "y"]
    resources = await server.mcp.get_resources()
    res = resources["resource://precommit-output"]
    out = await res.fn()
    assert out == "x\ny"
