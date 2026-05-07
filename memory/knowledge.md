# Knowledge

- API Azure DevOps Cloud v7.1.
- Objetos P0: Work Items y Wiki.
- Export primario: Markdown con manifest JSON.
- En `work-item search`, si el path ya contiene query params, `api-version` debe agregarse con `&` y no con `?` para evitar `ADO 400` (`WorkItemExpand` inválido).
- En búsquedas por texto (`--query`), escapar comillas simples en WIQL (`'` -> `''`) evita errores 400 por consulta malformada.
