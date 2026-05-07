# Baseline v0.1 — `ato-skill-ado-cli`

> Charter técnico, operativo y fundacional para construir el skill **Azure DevOps CLI** activado por `@ado`.

---

## 1. Identidad del Skill

| Campo | Valor |
|---|---|
| Nombre del skill | `ato-skill-ado-cli` |
| Versión baseline | `v0.1` |
| Baseline mode | **Baseline B — CLI Skill with External Services** |
| Comando/binario principal | `ato-skill-ado-cli` |
| Activación explícita corta | `@ado` |
| Stack objetivo | Python |
| Proveedor externo | Azure DevOps Cloud |
| Azure DevOps Server on-prem | Fuera de alcance v0.1 |
| Formato primario | Markdown (`.md`) |
| Formato máquina | JSON |
| Modo operativo por defecto | Read-only |
| Operaciones write | Permitidas solo para Work Items individuales, bajo demanda explícita |
| HTTPS | No incluido en v0.1 |
| MCP | Referenciado para evolución futura |

---

## 2. Propósito

`ato-skill-ado-cli` es un skill CLI de integración con **Azure DevOps Cloud**, activado por `@ado`, orientado a buscar, recuperar, catalogar, normalizar y exportar información de proyectos Azure DevOps.

Su propósito principal es producir artefactos estructurados —principalmente Markdown y manifiestos JSON— que puedan ser usados por:

- usuarios humanos,
- scripts,
- agentes de codificación IA,
- otros skills especializados,
- flujos posteriores de análisis, documentación o transformación.

El skill no debe tomar decisiones de negocio ni reemplazar el criterio de otros skills especializados. Su responsabilidad principal es **abrirse camino entre objetos Azure DevOps, recuperar contexto confiable y entregarlo en formatos reutilizables**.

---

## 3. Fórmula del Skill

El skill cumple la fórmula mínima:

```txt
Skill = tarea repetible + conocimiento contextual + procedimiento verificable + salida estándar
```

| Elemento | Definición |
|---|---|
| Tarea repetible | Buscar, recuperar, catalogar y exportar objetos Azure DevOps |
| Conocimiento contextual | Organización, proyecto ADO, Work Items, Wiki, relaciones, metadatos, plantillas |
| Procedimiento verificable | CLI, logs, manifiestos JSON, códigos de salida, validaciones `doctor` y `validate` |
| Salida estándar | Markdown + JSON |

---

## 4. Criterio de Decisión del Skill

El skill debe activarse cuando la intención del usuario o de una máquina sea:

- consultar Azure DevOps,
- buscar Work Items,
- recuperar detalles de Work Items,
- consultar páginas Wiki,
- exportar información ADO a Markdown,
- generar manifiestos JSON de recuperación/exportación,
- preparar contexto para otro skill,
- realizar una operación CRUD puntual sobre un Work Item específico.

El skill no debe activarse para tareas genéricas de análisis, diseño, decisión técnica, interpretación estratégica o modificación masiva.

---

## 5. Modelo de Activación

### 5.1 Activación Explícita

El patrón técnico explícito es:

```txt
@ado <acción>
```

Ejemplos:

```txt
@ado buscar work items sobre autenticación
@ado exportar wiki Architecture
@ado obtener work item 12345
@ado actualizar work item 12345
```

### 5.2 Activación por Lenguaje Natural

Cuando el skill esté cargado, también puede activarse por intención semántica.

Ejemplos:

```txt
Busca en Azure DevOps los work items relacionados con OAuth.
Exporta la wiki de arquitectura del proyecto.
Recupera el detalle del work item 12345.
Trae los artículos ADO para que otro skill los analice.
Actualiza puntualmente este Work Item con el campo indicado.
```

### 5.3 Activación por Máquina o Script

Ejemplos:

```bash
ato-skill-ado-cli work-item search --query "authentication" --json
ato-skill-ado-cli work-item get --id 12345 --format md
ato-skill-ado-cli wiki export --path "Architecture" --out exports/ado/wiki/architecture
ato-skill-ado-cli context --json
ato-skill-ado-cli capabilities --json
```

### 5.4 Activación de Descubrimiento de Contexto

Uso humano:

```bash
ato-skill-ado-cli ask "¿Cómo uso este skill?"
ato-skill-ado-cli context
ato-skill-ado-cli usage
ato-skill-ado-cli examples
```

Uso máquina:

```bash
ato-skill-ado-cli context --json
ato-skill-ado-cli capabilities --json
ato-skill-ado-cli schema --json
```

### 5.5 Activación Ambigua

Si la intención parece relacionada con Azure DevOps pero no contiene suficiente información, el skill debe pedir delimitación mínima.

Ejemplos ambiguos:

```txt
Busca algo en ADO.
Mira este proyecto.
Actualiza el item.
Exporta la documentación.
```

Respuesta esperada:

```txt
Necesito organización/proyecto configurado o explícito, tipo de objeto y criterio de búsqueda.
```

### 5.6 No Activación

No debe activarse cuando la solicitud sea demasiado general o fuera de dominio.

Ejemplos:

```txt
Ayúdame a programar.
Mejora este diseño.
Decide qué arquitectura usar.
Haz un resumen inteligente.
```

---

## 6. Cuándo Usarlo

Usar `ato-skill-ado-cli` cuando se necesite:

- consultar objetos Azure DevOps Cloud,
- recuperar Work Items,
- consultar o exportar Wiki,
- catalogar información del proyecto,
- generar archivos Markdown desde contenido ADO,
- generar manifiestos JSON para consumo por máquinas,
- preparar contexto para otro skill,
- validar conectividad y permisos de Azure DevOps,
- realizar un CRUD puntual sobre un Work Item específico.

---

## 7. Cuándo No Usarlo

No usar este skill para:

- decidir prioridades de producto,
- interpretar estrategia de arquitectura,
- escribir código de aplicación,
- modificar repositorios Git,
- ejecutar mutaciones masivas,
- cambiar Wiki en v0.1,
- operar Azure DevOps Server on-prem,
- administrar usuarios, permisos u organizaciones,
- reemplazar análisis humano,
- actuar como agente autónomo de gestión de proyectos.

---

## 8. Contexto Operativo del Skill

El skill debe conocer y exponer:

- nombre del skill,
- versión,
- baseline mode,
- organización Azure DevOps Cloud,
- proyecto Azure DevOps objetivo,
- scopes esperados del PAT,
- rutas de workspace,
- rutas de exportación,
- comandos disponibles,
- capacidades disponibles,
- servicios externos configurables,
- formato de salida,
- reglas de seguridad,
- límites de uso,
- códigos de salida,
- rutas relevantes del repositorio.

---

## 9. Contexto del Repositorio

El repositorio que implementa el skill es distinto del proyecto Azure DevOps consultado.

Se deben separar tres conceptos:

| Concepto | Significado |
|---|---|
| Skill repo project | Repositorio donde vive `ato-skill-ado-cli` |
| ADO organization | Organización Azure DevOps Cloud, por ejemplo `https://dev.azure.com/<org>` |
| ADO project | Proyecto Azure DevOps objetivo consultado u operado por el skill |

El **ADO project** debe ser parte de la configuración porque normalmente los PATs y permisos son atómicos o acotados por proyecto, scope y política organizacional.

---

## 10. Estructura Recomendada del Repositorio

```txt
repo/
  AGENTS.md
  README.md
  SKILL.md
  CHANGELOG.md
  Makefile
  .env.example
  config.example.yaml
  .gitignore

  docs/
    architecture.md
    activation.md
    cli.md
    validation.md
    security.md
    configuration.md
    context-discovery.md
    scope-governance.md
    services.md
    ado-cloud.md
    work-items.md
    wiki.md
    exports.md
    write-operations.md
    mcp-bridge.md

  cli/
    README.md
    ato_skill_ado_cli/

  bin/
    ato-skill-ado-cli

  scripts/
    install.sh
    bootstrap.sh
    validate.sh
    doctor.sh
    install-services.sh

  services/
    README.md
    azure-devops/
      README.md
      azure-devops.env.example
      azure-devops.config.example.yaml
      examples/
        work-item-search.request.json
        work-item-search.response.json
        wiki-export.request.json
        wiki-export.response.json
      mocks/
        sample-work-item.json
        sample-wiki-page.json

  contracts/
    input.schema.json
    output.schema.json
    service-request.schema.json
    service-response.schema.json
    capabilities.schema.json
    context.schema.json
    manifest.schema.json
    work-item.schema.json
    wiki-page.schema.json

  examples/
    invocation.md
    natural-language.md
    machine-cli.md
    context-discovery.md
    work-items.md
    wiki.md
    write-work-item.md
    inputs/
    outputs/

  templates/
    markdown/
      work-item.md.j2
      wiki-page.md.j2
      export-index.md.j2
    json/
      manifest.json.j2

  workspace/
    ado/
      cache/
        .gitkeep
      staging/
        .gitkeep
      manifests/
        .gitkeep
      doctor/
        .gitkeep
      sessions/
        .gitkeep

  exports/
    ado/
      work-items/
        .gitkeep
      wiki/
        .gitkeep
      bundles/
        .gitkeep

  memory/
    knowledge.md
    decisions.md
    iteration-history.md

  harnesses/
    restrictions.md
    behavior-limits.md
    safety-rules.md
    acceptance-checks.md
    write-guardrails.md

  logs/
    ado/
      .gitkeep

  tmp/
    ado/
      .gitkeep

  .github/
    copilot-instructions.md

  .agents/
    skills/
      ato-skill-ado-cli/
        SKILL.md
        scripts/
        examples/
```

---

## 11. Requisitos Fundacionales No Negociables

1. Deben existir manifiestos y documentación raíz.
2. Debe existir `SKILL.md` con frontmatter `name` y `description`.
3. El comando clave de activación es `@ado`.
4. El binario principal es `ato-skill-ado-cli`.
5. La CLI es obligatoria y es el núcleo operativo.
6. El modo por defecto es read-only.
7. Las operaciones write requieren solicitud explícita del usuario.
8. Las operaciones write v0.1 solo aplican a Work Items individuales.
9. No se permiten escrituras masivas.
10. No se permite Wiki write en v0.1.
11. No se permite Repos write en v0.1.
12. El proveedor soportado es Azure DevOps Cloud.
13. Azure DevOps Server on-prem queda fuera de alcance.
14. El formato primario de exportación es Markdown.
15. Todo export debe generar manifiesto JSON.
16. Deben existir plantillas `.env.example` y `config.example.yaml`.
17. No se deben versionar secretos.
18. Deben existir logs sin secretos.
19. Deben existir mocks offline.
20. Deben existir harnesses de restricciones y comportamiento.
21. Debe existir `doctor` para validar configuración, permisos y conectividad.
22. Debe existir `validate` para validar estructura, outputs y contratos.
23. El skill debe poder operar por humanos y por máquinas.
24. El skill debe exponer contexto de uso mediante CLI.
25. Las decisiones de alcance deben quedar registradas en memoria versionable.

---

## 12. Matriz de Alcance por Versión

### P0 — Obligatorio para v0.1

| Área | Alcance |
|---|---|
| CLI | `ato-skill-ado-cli` |
| Activación | `@ado` y lenguaje natural equivalente |
| Configuración | `.env`, variables de entorno, `config.yaml` |
| Auth | PAT Azure DevOps |
| Azure DevOps | Cloud solamente |
| Proyecto ADO | Configurable por defecto |
| Work Items | Search, get, export, create, update, delete puntual bajo guardrails |
| Wiki | List, get, export read-only |
| Export | Markdown + manifest JSON |
| Context discovery | `context`, `capabilities`, `usage`, `examples`, `schema` |
| Diagnóstico | `doctor` |
| Validación | `validate` |
| Workspace | `workspace/ado/` |
| Export nativo | `exports/ado/` |
| Logs | `logs/ado/` |
| Temporales | `tmp/ado/` |
| Mocks | Azure DevOps mocks offline |
| Seguridad | no secretos en logs, write explícito, dry-run |
| Memoria | decisiones, conocimiento, historial |
| Harnesses | restricciones, límites, aceptación, write guardrails |

### P1 — Recomendado para evolución cercana

| Área | Alcance |
|---|---|
| Repos | listar repos, leer archivos, exportar documentación |
| Pull Requests | lectura, recuperación y exportación |
| Commits | lectura y exportación |
| Queries WIQL | soporte avanzado |
| Bundles | paquetes exportables para otros skills |
| Cache | cache configurable con TTL |
| Plantillas | custom templates |
| Integración downstream | estructura estándar para consumo por otros skills |

### P2 — Interoperabilidad avanzada

| Área | Alcance |
|---|---|
| HTTPS | mini-servidor local |
| Endpoints | `/context`, `/capabilities`, `/run`, `/validate` |
| MCP | bridge funcional |
| Adapters | adaptadores para agentes externos |
| Contratos HTTP | esquemas request/response |
| Certificados locales | si HTTPS aplica |
| Seguridad red | autenticación local, allowlist, no exposición pública por defecto |

### P3 — Distribución y madurez

| Área | Alcance |
|---|---|
| Homebrew | fórmula publicada |
| CI/CD | pipeline completo |
| Paquete | distribución instalable |
| Hardening | seguridad avanzada |
| Documentación pública | sitio o catálogo interno |
| Compatibilidad | matriz de versiones Python/Azure DevOps API |

---

## 13. Decisiones Explícitas sobre HTTPS, Servicios Externos y MCP

### HTTPS

```txt
Decisión v0.1: No incluido.
Motivo: el skill debe estabilizar primero su contrato CLI, recuperación y exportación.
```

### Servicios Externos

```txt
Decisión v0.1: Sí incluido.
Servicio principal: Azure DevOps Cloud REST API.
Autenticación: PAT.
```

### MCP

```txt
Decisión v0.1: Referenciado para evolución futura.
No se implementa bridge MCP funcional.
Se debe conservar estructura documental para no bloquear evolución.
```

---

## 14. Decisiones Fuera de Alcance para v0.1

Queda fuera de alcance:

- Azure DevOps Server on-prem.
- Mini-servidor HTTPS.
- Bridge MCP funcional.
- Repositorios Git.
- Pull Requests.
- Commits.
- Pipelines.
- Mutaciones masivas.
- Wiki write.
- Repos write.
- Administración de usuarios.
- Administración de permisos.
- Gestión de organizaciones.
- Operación cross-project masiva.
- UI web.
- ejecución remota.
- scheduler interno.
- razonamiento estratégico autónomo.
- decisiones de negocio.
- auto-corrección de objetos ADO sin confirmación humana.

---

## 15. Arquitectura Técnica Mínima

### 15.1 Documentation Layer

Contiene:

- `README.md`
- `SKILL.md`
- `AGENTS.md`
- `CHANGELOG.md`
- `docs/`

### 15.2 Execution Layer

Contiene:

- `cli/`
- `bin/`
- `scripts/`
- `Makefile`

Responsabilidades:

- ejecutar CLI,
- validar configuración,
- invocar servicios,
- normalizar respuestas,
- exportar artefactos,
- producir logs y manifiestos.

### 15.3 Service Layer

Contiene:

- `services/azure-devops/`
- contratos,
- configuración,
- mocks,
- adaptadores.

Responsabilidades:

- encapsular llamadas Azure DevOps REST API,
- manejar autenticación PAT,
- paginar,
- recuperar objetos,
- normalizar errores,
- respetar límites y timeouts.

### 15.4 Compatibility Layer

En v0.1 solo documental y preparatoria:

- `docs/mcp-bridge.md`
- `contracts/`
- `schemas/` si se decide separarlos luego.

No debe implementar servidor ni MCP funcional.

---

## 16. Interfaz CLI Dual Humano/Máquina

### 16.1 Comandos Base

```bash
ato-skill-ado-cli init
ato-skill-ado-cli config init
ato-skill-ado-cli doctor
ato-skill-ado-cli validate
ato-skill-ado-cli context
ato-skill-ado-cli capabilities
ato-skill-ado-cli usage
ato-skill-ado-cli examples
ato-skill-ado-cli schema
ato-skill-ado-cli version
ato-skill-ado-cli logs
```

### 16.2 Comandos Work Item

```bash
ato-skill-ado-cli work-item search --query "authentication"
ato-skill-ado-cli work-item search --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.State] = 'Active'" --json
ato-skill-ado-cli work-item get --id 12345
ato-skill-ado-cli work-item export --id 12345 --out exports/ado/work-items/12345
ato-skill-ado-cli work-item create --type UserStory --title "New story" --write --dry-run
ato-skill-ado-cli work-item update --id 12345 --field "System.Tags" --value "reviewed" --write --dry-run
ato-skill-ado-cli work-item delete --id 12345 --write --dry-run
```

### 16.3 Comandos Wiki

```bash
ato-skill-ado-cli wiki list
ato-skill-ado-cli wiki get --path "Architecture"
ato-skill-ado-cli wiki export --path "Architecture" --out exports/ado/wiki/architecture
```

### 16.4 Comandos de Servicio

```bash
ato-skill-ado-cli service list
ato-skill-ado-cli service doctor azure-devops
ato-skill-ado-cli service config init azure-devops
```

### 16.5 Human CLI Mode

Debe permitir:

```bash
ato-skill-ado-cli ask "busca work items relacionados con OAuth"
ato-skill-ado-cli ask "exporta la wiki de arquitectura"
ato-skill-ado-cli ask "¿Cómo uso este skill?"
```

Debe priorizar:

- claridad,
- mensajes comprensibles,
- explicación de errores,
- sugerencias de siguiente paso,
- confirmación ante riesgo,
- no imprimir secretos.

### 16.6 Machine CLI Mode

Debe permitir:

```bash
ato-skill-ado-cli work-item get --id 12345 --json
ato-skill-ado-cli wiki export --path "Architecture" --out tmp/ado/wiki --manifest-json
ato-skill-ado-cli doctor --ci --json
ato-skill-ado-cli validate --format json
ato-skill-ado-cli context --json
ato-skill-ado-cli capabilities --json
```

Debe priorizar:

- salidas JSON parseables,
- códigos de salida estables,
- modo no interactivo,
- parámetros explícitos,
- logs estructurados,
- compatibilidad CI/CD.

---

## 17. Contexto de Uso Expuesto por CLI

`ato-skill-ado-cli context` debe exponer:

- propósito del skill,
- versión,
- baseline mode,
- organización ADO configurada,
- proyecto ADO configurado,
- comandos disponibles,
- capacidades disponibles,
- servicios disponibles,
- rutas de workspace,
- rutas de export,
- variables de entorno esperadas,
- archivos de configuración esperados,
- plantillas disponibles,
- ejemplos humanos,
- ejemplos máquina,
- reglas de seguridad,
- restricciones de comportamiento,
- validaciones disponibles,
- códigos de salida.

Ejemplo:

```bash
ato-skill-ado-cli context --json
```

Debe devolver JSON válido y no contener secretos.

---

## 18. Mini-servidor HTTPS

```txt
Decisión v0.1: No aplica.
```

El skill no debe implementar `ato-skill-ado-cli serve` en v0.1.

Debe documentarse como posible evolución P2.

---

## 19. Mini-servidores de Servicios Externos

```txt
Decisión v0.1: No aplica.
```

Los servicios externos se invocan desde CLI mediante adaptadores internos.

---

## 20. Integración con APIs de Terceros

### Servicio: Azure DevOps Cloud

| Campo | Valor |
|---|---|
| Nombre | `azure-devops` |
| Proveedor | Azure DevOps Cloud |
| URL base | `https://dev.azure.com/{organization}` |
| Auth | PAT |
| Proyecto | Configurable por defecto |
| API version sugerida | `7.1` |
| Objetos P0 | Work Items, Wiki |
| Objetos diferidos | Repos, PRs, Commits, Pipelines |

### Contrato del Servicio

Debe documentar:

- nombre,
- propósito,
- URL base,
- modo de autenticación,
- variables requeridas,
- configuración requerida,
- entradas,
- salidas,
- errores conocidos,
- límites,
- timeouts,
- reintentos,
- mocks,
- pruebas offline,
- reglas de seguridad.

---

## 21. Bridge MCP

```txt
Estado v0.1: Referenciado para evolución futura.
```

Debe existir documentación que indique:

- posibles capacidades futuras,
- mapeo conceptual CLI → MCP,
- acciones permitidas futuras,
- acciones prohibidas,
- restricción de no ampliar permisos,
- dependencia de aprobación humana para implementación funcional.

No debe existir bridge funcional en v0.1.

---

## 22. Procedimiento Operativo

### 22.1 Primer Uso

```bash
make install
make bootstrap
ato-skill-ado-cli config init
ato-skill-ado-cli doctor
ato-skill-ado-cli context
```

### 22.2 Flujo de Lectura

```bash
ato-skill-ado-cli work-item search --query "OAuth"
ato-skill-ado-cli work-item get --id 12345 --format md
ato-skill-ado-cli work-item export --id 12345 --out exports/ado/work-items/12345
```

### 22.3 Flujo Wiki

```bash
ato-skill-ado-cli wiki list
ato-skill-ado-cli wiki get --path "Architecture"
ato-skill-ado-cli wiki export --path "Architecture" --out exports/ado/wiki/architecture
```

### 22.4 Flujo Write Controlado

Toda operación write debe iniciar en dry-run.

```bash
ato-skill-ado-cli work-item update   --id 12345   --field "System.Tags"   --value "architecture-review"   --write   --dry-run
```

Ejecución confirmada:

```bash
ato-skill-ado-cli work-item update   --id 12345   --field "System.Tags"   --value "architecture-review"   --write   --yes
```

Debe generar:

- log de operación,
- manifiesto JSON,
- resumen Markdown si aplica,
- evidencia del request normalizado,
- evidencia de respuesta sin secretos.

---

## 23. Validaciones Verificables

### Comandos

```bash
make validate
make test
make doctor
ato-skill-ado-cli validate
ato-skill-ado-cli doctor
ato-skill-ado-cli doctor --ci --json
```

### Evidencias Esperadas

- JSON válido,
- códigos de salida,
- logs,
- manifiestos,
- archivos Markdown generados,
- resultados de mocks,
- validación de plantillas,
- validación de `.gitignore`,
- validación de ausencia de secretos en logs.

### Códigos de Salida

| Código | Significado |
|---|---|
| `0` | Éxito |
| `1` | Error general |
| `2` | Configuración inválida |
| `3` | Autenticación fallida |
| `4` | Permisos insuficientes |
| `5` | Objeto no encontrado |
| `6` | Error de validación |
| `7` | Operación write bloqueada |
| `8` | Error de red o timeout |
| `9` | Contrato de salida inválido |

---

## 24. Reglas de Seguridad

1. No imprimir PAT en consola.
2. No registrar PAT en logs.
3. No versionar `.env`.
4. No versionar configuraciones locales sensibles.
5. Usar scopes mínimos de PAT.
6. El modo por defecto es read-only.
7. Toda escritura requiere `--write`.
8. Toda escritura debe soportar `--dry-run`.
9. Toda escritura real requiere confirmación humana o `--yes` explícito.
10. `--yes` solo se permite con parámetros deterministas completos.
11. No permitir bulk update en v0.1.
12. No permitir Wiki write en v0.1.
13. No permitir Repos write en v0.1.
14. No exponer rutas arbitrarias del sistema.
15. No escribir fuera de workspace/export path autorizado.
16. No ejecutar shell arbitrario.
17. No inferir cambios de negocio.
18. No encadenar operaciones write.
19. No modificar múltiples Work Items en una sola operación.
20. No ocultar errores de permisos.

---

## 25. Dependencias e Instalación Cross-platform

### Dependencias Base

- Python 3.11+
- `venv` requerido para desarrollo local
- `make`
- `curl`
- `jq` opcional para pruebas JSON

### Instalación Recomendada

```bash
./setup-skill.sh
source .venv/bin/activate
ato-skill-ado-cli capabilities --json
```

### Instalación Manual

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e ".[dev]"
ato-skill-ado-cli doctor --json
```

### Nota PEP 668 y Homebrew Python

No instalar dependencias con `pip` global del sistema. En macOS con Python gestionado
por Homebrew, eso dispara `externally-managed-environment` (PEP 668). La instalación
debe ocurrir dentro de `.venv` (vía `make install` o instalación manual con venv).

El soporte para fórmula `brew install ato-skill-ado-cli` se mantiene como posible
evolución futura, fuera del alcance de esta fase.

---

## 26. Variables de Entorno y Configuración

### `.env.example`

```bash
ADO_ORGANIZATION=
ADO_PROJECT=
ADO_PAT=
ADO_API_VERSION=7.1

ADO_DEFAULT_OUTPUT=md
ADO_WORKSPACE_DIR=workspace/ado
ADO_EXPORT_DIR=exports/ado
ADO_LOG_DIR=logs/ado
ADO_TMP_DIR=tmp/ado

ADO_LOG_LEVEL=info
ADO_TIMEOUT_SECONDS=30
ADO_MAX_RESULTS=100
ADO_WRITE_ENABLED=false
ADO_REQUIRE_DRY_RUN=true
```

### `config.example.yaml`

```yaml
azure_devops:
  organization: ""
  project: ""
  api_version: "7.1"
  auth:
    pat_env_var: "ADO_PAT"

defaults:
  output: "md"
  workspace_dir: "workspace/ado"
  export_dir: "exports/ado"
  log_dir: "logs/ado"
  tmp_dir: "tmp/ado"
  max_results: 100
  timeout_seconds: 30

write_policy:
  enabled: false
  require_write_flag: true
  require_dry_run: true
  require_confirmation: true
  allowed_objects:
    - work_item
  forbidden_objects:
    - wiki
    - repo
    - pull_request
    - pipeline
  allow_bulk: false
```

### Precedencia de Configuración

```txt
1. Argumento CLI explícito
2. Variable de entorno
3. Archivo .env local
4. config.yaml local
5. default seguro
```

---

## 27. Plantillas `.env.example` y Config Examples

Deben existir:

```txt
.env.example
config.example.yaml
services/azure-devops/azure-devops.env.example
services/azure-devops/azure-devops.config.example.yaml
```

Archivos locales no versionables:

```txt
.env
.env.local
config.yaml
config.local.yaml
services/azure-devops/azure-devops.env
services/azure-devops/azure-devops.config.yaml
```

---

## 28. Logs, Temporales y Trazabilidad

### Rutas

```txt
logs/ado/
tmp/ado/
workspace/ado/sessions/
workspace/ado/manifests/
workspace/ado/doctor/
```

### Reglas

- Los logs no deben contener secretos.
- Cada export debe generar manifiesto JSON.
- Cada write debe generar evidencia.
- Cada doctor debe generar diagnóstico verificable.
- Los temporales deben poder limpiarse sin romper el repositorio.
- Los manifiestos pueden copiarse junto con exports permanentes.

---

## 29. Memoria de Conocimiento

Debe existir:

```txt
memory/
  knowledge.md
  decisions.md
  iteration-history.md
```

### `memory/knowledge.md`

Debe registrar conocimiento operativo estable:

- convenciones ADO,
- campos comunes de Work Items,
- reglas de exportación,
- límites conocidos.

### `memory/decisions.md`

Debe registrar decisiones aceptadas y diferidas.

### `memory/iteration-history.md`

Debe registrar evolución de baseline.

---

## 30. Harnesses de Restricciones, Límites y Comportamiento

Debe existir:

```txt
harnesses/
  restrictions.md
  behavior-limits.md
  safety-rules.md
  acceptance-checks.md
  write-guardrails.md
```

### Harness Write Guardrails

Debe validar:

- write sin `--write` bloqueado,
- write sin `--dry-run` inicial bloqueado,
- bulk write bloqueado,
- wiki write bloqueado,
- repo write bloqueado,
- delete work item requiere confirmación explícita,
- logs no contienen PAT,
- salida JSON contiene manifiesto de operación.

---

## 31. Plantillas Example

### Work Item Markdown

```md
# Work Item {{ id }} — {{ title }}

| Campo | Valor |
|---|---|
| ID | {{ id }} |
| Tipo | {{ type }} |
| Estado | {{ state }} |
| Asignado a | {{ assigned_to }} |
| Área | {{ area_path }} |
| Iteración | {{ iteration_path }} |
| Tags | {{ tags }} |

## Descripción

{{ description }}

## Criterios de Aceptación

{{ acceptance_criteria }}

## Relaciones

{{ relations }}

## Metadatos de Exportación

- Organización: `{{ organization }}`
- Proyecto: `{{ project }}`
- Exportado en: `{{ exported_at }}`
- Manifiesto: `{{ manifest_path }}`
```

### Export Manifest JSON

```json
{
  "skill": "ato-skill-ado-cli",
  "baseline_version": "v0.1",
  "operation": "export",
  "provider": "azure-devops-cloud",
  "organization": "",
  "project": "",
  "object_type": "",
  "object_id": "",
  "output_files": [],
  "created_at": "",
  "source_url": "",
  "warnings": [],
  "errors": []
}
```

---

## 32. Reglas de `.gitignore`

Debe excluir:

```gitignore
# Logs and temporary files
logs/*
tmp/*
workspace/ado/cache/*
workspace/ado/staging/*
workspace/ado/doctor/*
workspace/ado/sessions/*

# Local secrets and config
.env
.env.local
.env.*.local
config.yaml
config.local.yaml
*.local.yaml
*.local.json

# Service local secrets/config
services/*/*.env
services/*/*.config.yaml
services/*/*.local.yaml

# Logs
*.log

# Python
__pycache__/
*.py[cod]
.pytest_cache/
.mypy_cache/
.ruff_cache/
.venv/
venv/
dist/
build/
*.egg-info/

# Node or generic tooling if added later
node_modules/

# Cache
.cache/
```

Debe permitir conservar estructura y plantillas:

```gitignore
!logs/**/.gitkeep
!tmp/**/.gitkeep
!workspace/**/.gitkeep
!.env.example
!config.example.yaml
!services/*/*.env.example
!services/*/*.config.example.yaml
!exports/**/.gitkeep
```

---

## 33. Historial de Iteraciones

### v0.1

| Campo | Valor |
|---|---|
| Versión | `v0.1` |
| Cambio | Creación de baseline fundacional |
| Motivo | Definir charter técnico y operativo para construir el repositorio del skill |
| Impacto esperado | Permitir implementación ordenada, verificable y evolutiva |
| Decisiones aceptadas | Python, Baseline B, Azure DevOps Cloud, `@ado`, Work Items + Wiki, Markdown + JSON |
| Decisiones diferidas | Repos, HTTPS, MCP funcional, Azure DevOps Server, PRs, pipelines |
| Pendientes abiertos | Validar scopes mínimos exactos de PAT, definir librerías Python, seleccionar framework CLI |

---

## 34. Próximos Pasos

1. Crear repositorio base.
2. Crear archivos raíz:
   - `README.md`
   - `SKILL.md`
   - `AGENTS.md`
   - `CHANGELOG.md`
3. Crear estructura de carpetas.
4. Implementar CLI mínima en Python.
5. Implementar `config init`.
6. Implementar `doctor`.
7. Implementar cliente Azure DevOps Cloud read-only.
8. Implementar Work Item search/get/export.
9. Implementar Wiki list/get/export.
10. Implementar manifests JSON.
11. Implementar write guardrails para Work Items.
12. Implementar mocks offline.
13. Implementar harnesses.
14. Ejecutar `make validate`.
15. Registrar primera iteración en `memory/iteration-history.md`.

---

## 35. Criterios de Aceptación v0.1

La baseline v0.1 se considera implementada cuando:

- `ato-skill-ado-cli doctor` valida configuración y conexión.
- `ato-skill-ado-cli context --json` devuelve JSON válido.
- `ato-skill-ado-cli capabilities --json` devuelve capacidades reales.
- `ato-skill-ado-cli work-item search` consulta Azure DevOps Cloud.
- `ato-skill-ado-cli work-item get` recupera un Work Item.
- `ato-skill-ado-cli work-item export` genera Markdown y manifest JSON.
- `ato-skill-ado-cli wiki list` lista Wikis.
- `ato-skill-ado-cli wiki get` recupera una página.
- `ato-skill-ado-cli wiki export` genera Markdown y manifest JSON.
- Las operaciones write sobre Work Items requieren `--write`.
- Las operaciones write soportan `--dry-run`.
- Las operaciones write no permiten bulk.
- Los logs no contienen PAT.
- Los mocks offline permiten pruebas sin Azure DevOps.
- `make validate` ejecuta validaciones estructurales.
- La documentación raíz permite a un agente constructor implementar el repositorio sin reinterpretar el alcance.

---

## 36. Síntesis Ejecutiva

`ato-skill-ado-cli` v0.1 será un skill Python CLI de integración con Azure DevOps Cloud, activado por `@ado`, diseñado para recuperar, catalogar y exportar Work Items y Wiki principalmente en Markdown con manifiestos JSON.

Su modo predeterminado será read-only. Las operaciones write se permitirán únicamente sobre Work Items individuales, de forma explícita, puntual y gobernada por guardrails. Repos, HTTPS, MCP funcional y Azure DevOps Server quedan fuera de alcance para evitar complejidad accidental en la primera versión.
