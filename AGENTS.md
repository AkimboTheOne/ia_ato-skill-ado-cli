# AGENTS

- Activación explícita: `@ado`.
- Binario principal: `ato-skill-ado-cli`.
- Modo por defecto: read-only.
- Write solo para Work Items individuales y con `--write`.

## Operación esperada

- Ejecutar primero `doctor` para validar configuración y autenticación.
- Priorizar comandos read para recuperación y export.
- Escribir solo bajo solicitud explícita y respetando guardrails (`--dry-run` antes de `--yes`).

## Alcance actual (v0.2 / P1)

- Work Items: search, wiql, get, export, create, update, delete.
- Wiki: list, get, export (read-only).
- Repos: list, get-file, export (read-only).
- Pull Requests: list, export (read-only).
- Commits: list, export (read-only).
- Bundle: export de contexto consolidado.
