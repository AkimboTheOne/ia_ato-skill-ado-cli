# Decisions

## v0.1 (baseline)

- CLI Python con Typer + Pydantic.
- Azure DevOps Cloud como único proveedor soportado.
- Modo operativo por defecto: read-only.
- Escritura permitida solo para Work Items individuales con guardrails.
- Wiki write, repo write y bulk write bloqueados.

## v0.2 (P1)

- Se amplía superficie read-only con Repos, Pull Requests y Commits.
- Se incorpora comando WIQL dedicado (`work-item wiql`) con salida normalizada.
- Se habilitan bundles de contexto para consumo downstream (`bundle export`).
- Se agrega caché local con TTL configurable para lecturas repetidas.
- Se habilita plantilla custom en export Markdown (`--template`) para `work-item` y `wiki`.
- Se prepara transición P2 con contrato `run` y validación de payload (`validate --payload-file`).
- Se preserva política de seguridad: write únicamente en Work Item individual y flujo explícito `--write` + `--dry-run` + `--yes`.
