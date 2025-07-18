"""FastMCP server streaming pre-commit output."""

import anyio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterable
from watchfiles import awatch

from fastmcp import FastMCP
from fastmcp.server.context import Context
import fastmcp

from .tools import run_precommit

LAST_OUTPUT: list[str] = []


async def _run_precommit_stream(
    ctx: Context | None = None, *, files: Iterable[str] | None = None
) -> None:
    """Run pre-commit and stream output via context logging."""
    global LAST_OUTPUT
    lines = await run_precommit(list(files) if files else None)
    LAST_OUTPUT = lines
    if ctx:
        for line in lines:
            await ctx.info(line)


async def _watch_changes() -> None:
    """Watch for file changes and run pre-commit."""
    async for changes in awatch(".", stop_event=None):
        files = [path for _, path in changes]
        if files:
            await _run_precommit_stream(files=files)


@asynccontextmanager
async def precommit_lifespan(app: FastMCP) -> AsyncIterator[None]:
    """Run pre-commit once at startup and expose output."""
    async with anyio.create_task_group() as tg:
        await _run_precommit_stream()
        tg.start_soon(_watch_changes)
        try:
            yield
        finally:
            tg.cancel_scope.cancel()


def _get_output() -> str:
    return "\n".join(LAST_OUTPUT)


mcp = FastMCP(
    "fast-precommit-mcp",
    instructions="Runs pre-commit continuously and exposes the output.",
    lifespan=precommit_lifespan,
)


@mcp.resource("resource://precommit-output", description="Latest pre-commit output")
async def precommit_output_resource() -> str:
    return _get_output()


@mcp.tool()
async def run_precommit_tool(ctx: Context, files: list[str] | None = None) -> str:
    """Run pre-commit optionally on specific files."""
    await _run_precommit_stream(ctx, files=files or None)
    return _get_output()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
