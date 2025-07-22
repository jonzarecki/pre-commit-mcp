# Fast Pre-commit MCP

[![CI](https://github.com/jonzarecki/pre-commit-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/jonzarecki/pre-commit-mcp/actions/workflows/ci.yml)

This repository contains a demonstration MCP server built with [FastMCP](https://pypi.org/project/fastmcp/). The server runs `pre-commit` once when it starts and then reruns it whenever files change. Output is streamed to connected MCP clients and can also be refreshed on demand using a tool.

## Installation

Install directly from GitHub with pip:

```bash
pip install git+https://github.com/jonzarecki/pre-commit-mcp
```

Run the server with `npx` without needing a system-wide install:

```bash
npx --yes github:jonzarecki/pre-commit-mcp
```

Or clone the repository and install in editable mode for development:

```bash
git clone https://github.com/jonzarecki/pre-commit-mcp.git
cd pre-commit-mcp
pip install -e .[dev]
```

## Usage

Run the server:

```bash
python -m fast_precommit_mcp.server
```

Available tools:

- `run_precommit_tool` – Executes `pre-commit run` (optionally on specific files) and streams log lines back to the client.

The latest pre-commit output is also available as a resource named `precommit-output`.

## MCP client configuration

To let an MCP client automatically install and launch the server, add the following to `mcp.json`:

```json
{
  "mcpServers": {
    "fast-precommit-mcp": {
      "command": "npx --yes github:jonzarecki/pre-commit-mcp",
      "env": {}
    }
  }
}
```
