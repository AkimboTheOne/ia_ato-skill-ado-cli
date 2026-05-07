# ato-skill-ado-cli

Skill CLI para Azure DevOps Cloud activado por `@ado`.

## Quickstart

```bash
make install
make bootstrap
ato-skill-ado-cli config init
ato-skill-ado-cli doctor --json
ato-skill-ado-cli capabilities --json
```

## Alcance v0.2 (P1)

- Work Items: `search`, `wiql`, `get`, `export`, `create`, `update`, `delete`.
- Wiki: `list`, `get`, `export` (read-only).
- Repos: `list`, `get-file`, `export` (read-only).
- Pull Requests: `list`, `export` (read-only).
- Commits: `list`, `export` (read-only).
- Bundle: `bundle export` para snapshot unificado downstream.

## Guardrails de escritura

- Default `read-only`.
- Write solo para Work Item individual.
- Requiere `--write` explícito.
- Requiere `--dry-run` antes de confirmación con `--yes`.
- Bloqueado: `bulk write`, `wiki write`, `repo write`.

## Cache de lectura

- TTL configurable: `defaults.cache_ttl_seconds` o `ADO_CACHE_TTL_SECONDS`.
- Ubicación por defecto: `workspace/ado/cache`.

## Contratos y manifiestos

- Contratos CLI/interop en `contracts/`.
- Exportes generan `manifest.json`.
- Preparación P2: `run --payload-file` y schemas `run.request/response`.
