# CLI to MCP Mapping (P2 prep)

## Objective

Define a stable conceptual mapping from CLI operations to an MCP-compatible execution contract without enabling a full MCP bridge yet.

## Contract shape

- Request schema: `contracts/run.request.schema.json`
- Response schema: `contracts/run.response.schema.json`
- Entry command: `ato-skill-ado-cli run --payload-file <path>`

## Current supported operations

- `context`
- `work-item.search`
- `wiql.query`

## Future endpoint compatibility

The contract is intentionally aligned to future endpoint semantics:

- `/context`
- `/capabilities`
- `/run`
- `/validate`
