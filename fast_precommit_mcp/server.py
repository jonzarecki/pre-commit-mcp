"""FastMCP server streaming pre-commit output."""

from __future__ import annotations

import anyio
from contextlib import asynccontextmanager
from typing import AsyncIterator, Iterable

from fastmcp import Context, FastMCP

from .tools import run_precommit

LAST_OUTPUT: list[str] = []


async def _changed_files() -> list[str]:
    """Return a list of files changed in the working tree."""
    process = await anyio.open_process(
        [
            "git",
            "status",
            "--porcelain",
        ],
        stdout=anyio.subprocess.PIPE,
    )
    assert process.stdout
    raw = await process.stdout.read()
    await process.wait()
    files = []
    for line in raw.decode().splitlines():
        if line:
            files.append(line[3:])
    return files


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
    """Continuously run pre-commit on modified files."""
    while True:
        files = await _changed_files()
        if files:
            await _run_precommit_stream(files=files)
        await anyio.sleep(2)


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


@mcp.resource("precommit-output", description="Latest pre-commit output")
async def precommit_output_resource() -> str:
    return _get_output()


@mcp.tool()
async def run_precommit_tool(ctx: Context, *files: str) -> str:
    """Run pre-commit optionally on specific files."""
    await _run_precommit_stream(ctx, files=files or None)
    return _get_output()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
