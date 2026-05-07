# Write Operations

Write operations are intentionally restricted.

## Allowed

- Work Item `create`, `update`, `delete` (single item).

## Mandatory safety flags

- `--write`
- `--dry-run` (first pass)
- `--yes` (confirmed execution)

## Forbidden

- bulk write
- wiki write
- repo write
