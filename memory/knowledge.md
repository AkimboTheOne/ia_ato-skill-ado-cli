# Knowledge

- API objetivo: Azure DevOps Cloud REST API `7.1`.
- Export primario: Markdown + manifest JSON.
- Operaciones read de P1: Work Items, Wiki, Repos, Pull Requests, Commits.
- Patrón de robustez en URL ADO: cuando hay query params se debe agregar `api-version` con `&`.
- Seguridad WIQL: en búsquedas por texto hay que escapar comillas simples (`'` -> `''`).
- Guardrails de write activos:
  - write explícito requerido (`--write`),
  - dry-run inicial requerido (`--dry-run`),
  - confirmación explícita para ejecutar (`--yes`),
  - no bulk write,
  - no wiki/repo write.
- Cache P1:
  - directorio por defecto: `workspace/ado/cache`,
  - key hash SHA-256,
  - TTL configurable por `defaults.cache_ttl_seconds` o `ADO_CACHE_TTL_SECONDS`.
