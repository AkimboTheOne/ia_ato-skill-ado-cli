# Iteration History

## v0.1

- Scaffold inicial del repositorio baseline.
- Implementación CLI dual humano/máquina.
- Integración ADO Cloud P0 + exportes + validaciones mínimas.
- Hotfix estabilidad `work-item search`: corrección de URL con query (`&api-version`) + escape de comillas en WIQL + tests de regresión (`tests/test_ado_client.py`).
- Validación smoke real con Azure DevOps: consulta WIQL por `Epic` devuelve resultados correctamente.
