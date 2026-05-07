# Services

## Primary external service

- Azure DevOps Cloud REST API

## Health checks

- `doctor`
- `service doctor --name azure-devops`

## Failure modes

- `401`: authentication failure (PAT invalid or missing scope).
- `403`: permission denied.
- `404`: object not found.
- network errors: DNS/connectivity/timeouts.
