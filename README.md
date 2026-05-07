# ato-skill-ado-cli

Skill CLI para Azure DevOps Cloud activado por `@ado`.

## Quickstart

```bash
./setup-skill.sh
source .venv/bin/activate
ato-skill-ado-cli capabilities --json
```

Alternativas equivalentes:

```bash
make setup
./scripts/setup.sh --with-tests
```

## Solución de problemas PEP 668 (externally-managed-environment)

Este repositorio no instala dependencias en el Python global del sistema.
`make install` crea/reutiliza un entorno virtual local en `.venv` e instala allí
`ato-skill-ado-cli` con dependencias de desarrollo, evitando el error de PEP 668
en instalaciones gestionadas por Homebrew u otros distribuidores.

Si necesitas verificar estado inicial:

```bash
./scripts/doctor.sh
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
