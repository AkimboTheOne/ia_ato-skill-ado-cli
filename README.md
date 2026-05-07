# ato-skill-ado-cli

CLI skill para Azure DevOps Cloud activado por `@ado`.

## Quickstart

```bash
make install
make bootstrap
ato-skill-ado-cli config init
ato-skill-ado-cli doctor
ato-skill-ado-cli context
```

## Alcance v0.2 (P1)

- Work Items: `search`, `wiql`, `get`, `export`, `create`, `update`, `delete`.
- Wiki: `list`, `get`, `export` (read-only).
- Repos: `list`, `get-file`, `export` (read-only).
- Pull Requests: `list`, `export` (read-only).
- Commits: `list`, `export` (read-only).
- Bundles: `bundle export` con snapshot unificado para downstream.
- Cache TTL configurable (`defaults.cache_ttl_seconds`, `ADO_CACHE_TTL_SECONDS`).
- Export custom templates con `--template` en `work-item export` y `wiki export`.
- Preparación P2: contrato `run` + `validate --payload-file` y esquemas `run.request/response`.

## Guardrails de escritura

- Default `read-only`.
- Write sólo para Work Item individual.
- Requiere `--write` explícito.
- Requiere `--dry-run` inicial antes de confirmar con `--yes`.
- Bulk write, wiki write y repo write bloqueados.
