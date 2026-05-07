---
name: ato-skill-ado-cli
description: Skill CLI de Azure DevOps Cloud (@ado) para recuperar, normalizar y exportar contexto técnico en Markdown + JSON con operación read-first y guardrails de escritura.
---

# Skill

`ato-skill-ado-cli` ofrece una interfaz CLI consistente para humanos y máquinas que necesitan recuperar información de Azure DevOps y transformarla en artefactos reutilizables.

## Capacidades

- Descubrimiento de contexto: `context`, `capabilities`, `usage`, `examples`, `schema`.
- Diagnóstico y validación: `doctor`, `validate`.
- Lectura y export:
  - Work Items, Wiki, Repos, Pull Requests y Commits.
- Bundles de contexto para flujos downstream.
- Contrato de ejecución inicial (`run`) para evolución a MCP.

## Reglas operativas

- Modo predeterminado `read-only`.
- Escrituras solo para Work Item individual con `--write` y flujo seguro.
- Prohibido bulk write, wiki write y repo write en v0.2.

## Onboarding Local

- Atajo recomendado: `./setup-skill.sh` (instala, bootstrap, config init, doctor y tests).
- Flujo alterno: `make setup` o `./scripts/setup.sh --with-tests`.
