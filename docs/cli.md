# CLI

## Main groups

- `work-item`
- `wiki`
- `repo`
- `pr`
- `commit`
- `bundle`
- `service`
- `config`

## Key commands

```bash
ato-skill-ado-cli doctor --json
ato-skill-ado-cli capabilities --json
ato-skill-ado-cli work-item wiql --query "SELECT [System.Id] FROM WorkItems"
ato-skill-ado-cli repo list --json
ato-skill-ado-cli bundle export --out exports/ado/bundles/latest
```

## Interop command

```bash
ato-skill-ado-cli run --payload-file payload.json --json
```
