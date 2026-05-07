# Security

## Principles

- No secrets in logs or exported artifacts.
- PAT is required but must be masked in diagnostics.
- Default mode is read-only.

## Write guardrails

- Write only for Work Item individual operations.
- `--write` is mandatory.
- `--dry-run` is mandatory before confirmed execution (`--yes`).
- Bulk write is forbidden.
- Wiki and Repo write are forbidden in v0.2.
