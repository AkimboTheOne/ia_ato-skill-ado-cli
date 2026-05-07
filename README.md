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

## Alcance v0.1

- Work Items: `search`, `get`, `export`, `create`, `update`, `delete` (write bajo guardrails).
- Wiki: `list`, `get`, `export` (read-only).
- Salidas: Markdown + manifiesto JSON.
- Diagnóstico: `doctor`.
- Validación: `validate`.

