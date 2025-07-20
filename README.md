# Fast Pre-commit MCP

[![CI](https://github.com/jonzarecki/pre-commit-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/jonzarecki/pre-commit-mcp/actions/workflows/ci.yml)

This repository contains a demonstration MCP server built with [FastMCP](https://pypi.org/project/fastmcp/). The server runs `pre-commit` once when it starts and then reruns it whenever files change. Output is streamed to connected MCP clients and can also be refreshed on demand using a tool.

## Usage

Run the server:

```bash
python -m fast_precommit_mcp.server
```

Available tools:

- `run_precommit_tool` – Executes `pre-commit run` (optionally on specific files) and streams log lines back to the client.

The latest pre-commit output is also available as a resource named `precommit-output`.
