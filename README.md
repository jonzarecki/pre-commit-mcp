# Fast Pre-commit MCP

[![CI](https://github.com/your-org/pre-commit-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/your-org/pre-commit-mcp/actions/workflows/ci.yml)

This repository contains a demonstration MCP server built with [FastMCP](https://pypi.org/project/fastmcp/). The server runs `pre-commit` once when it starts and then reruns it whenever files change. Output is streamed to connected MCP clients and can also be refreshed on demand using a tool.

## Usage

Run the server:

```bash
python -m fast_precommit_mcp.server
```

`watchfiles` is installed automatically so the server can monitor the repository
for changes without any additional configuration.

Available tools:

- `run_precommit_tool` – Executes `pre-commit run` (optionally on specific files) and streams log lines back to the client.

The latest pre-commit output is also available as a resource named `precommit-output`.

## Testing Plan

1. **Unit Tests**
   - Test that `run_precommit` returns a list of output lines.
   - Test that `_run_precommit_stream` updates `LAST_OUTPUT` and logs via a provided `Context` mock.
   - Test that the resource `precommit-output` returns the stored output.

2. **Integration Test**
   - Start the server using `FastMCP`'s `stdio` transport.
   - Verify that on startup the `precommit-output` resource contains pre-commit output.
   - Invoke `run_precommit_tool` via a client and check that new output is streamed as log messages and the resource updates.

3. **End‑to‑End Manual Test**
   - Initialize a git repository with a `.pre-commit-config.yaml`.
   - Install the hooks with `pre-commit install`.
   - Run the server and perform typical MCP interactions, ensuring log messages from pre‑commit appear in the conversation and the resource reflects the latest run.

GitHub Actions runs the lint and compile checks in `.github/workflows/ci.yml` on every push and pull request.
