# Architecture

## Core components

- `main.py`: CLI commands and orchestration.
- `core/ado_client.py`: Azure DevOps REST client.
- `core/write_policy.py`: guardrails for write operations.
- `core/cache.py`: read cache with TTL.
- `core/render.py`: template rendering + manifest writing.

## Runtime flow

1. Load config and environment.
2. Validate auth/context (`doctor`).
3. Execute read/write command.
4. Render output and emit manifest when exporting.

## Evolution boundary

- v0.2 keeps CLI as the single runtime interface.
- P2-ready contract exists via `run` command and JSON schemas.
