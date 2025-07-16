"""pre-commit tool functions."""

from __future__ import annotations

import asyncio
from typing import Any


async def run_precommit(files: list[str] | None = None) -> list[str]:
    """Run pre-commit and return output lines.

    If *files* is provided, only those paths are checked.
    """
    cmd = ["pre-commit", "run"]
    if files:
        cmd.append("--files")
        cmd.extend(files)

    process = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    lines: list[str] = []
    assert process.stdout
    async for raw in process.stdout:
        line = raw.decode().rstrip()
        lines.append(line)
    await process.wait()
    return lines
