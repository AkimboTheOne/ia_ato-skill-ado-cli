# Iteration History

## v0.1

- Scaffold inicial del baseline.
- CLI dual (uso humano y máquina).
- Integración ADO Cloud para Work Items + Wiki.
- Export Markdown + manifest JSON.
- Guardrails de write para Work Items.
- Hotfix de `work-item search`: query params y escape de comillas WIQL.

## v0.2 (P1)

- Nuevos comandos: `repo list|get-file|export`, `pr list|export`, `commit list|export`.
- Nuevo comando `work-item wiql` para consultas avanzadas.
- Nuevo comando `bundle export` para snapshot multi-objeto.
- Caché local de lectura en `workspace/ado/cache` con TTL configurable.
- Soporte de templates custom en export Markdown.
- Contratos iniciales para P2: `run.request.schema.json` y `run.response.schema.json`.
- Validación funcional con smoke test real ADO (read-only) sobre repos y commits.

## v0.2.2

- Se incorpora flujo de setup asistido unificado (`scripts/setup.sh`) con opción de tests.
- Se agrega atajo visible en raíz (`setup-skill.sh`) para mejorar discoverability en incorporación.
- Se endurece la instalación contra PEP 668 (venv local + detección Python >=3.11 + hints de brew).
