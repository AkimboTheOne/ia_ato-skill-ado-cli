from __future__ import annotations

from typing import Any

import requests
from urllib.parse import quote

from .errors import SkillError
from .models import AppConfig


class AzureDevOpsClient:
    def __init__(self, config: AppConfig, pat: str):
        self.config = config
        self.organization = config.azure_devops.organization
        self.project = config.azure_devops.project
        self.api_version = config.azure_devops.api_version
        self.timeout = config.defaults.timeout_seconds
        if not self.organization:
            raise SkillError("ADO_ORGANIZATION/config organization requerido", 2)
        if not self.project:
            raise SkillError("ADO_PROJECT/config project requerido", 2)
        if not pat:
            raise SkillError("PAT no configurado", 3)
        self.session = requests.Session()
        self.session.auth = ("", pat)

    def _url(self, path: str) -> str:
        sep = "&" if "?" in path else "?"
        return f"https://dev.azure.com/{self.organization}/{self.project}/_apis/{path}{sep}api-version={self.api_version}"

    def _request(self, method: str, path: str, json_body: dict[str, Any] | None = None) -> dict[str, Any]:
        try:
            response = self.session.request(method, self._url(path), json=json_body, timeout=self.timeout)
        except requests.RequestException as exc:
            raise SkillError(f"error de red: {exc}", 8) from exc
        if response.status_code == 401:
            raise SkillError("autenticación fallida", 3)
        if response.status_code == 403:
            raise SkillError("permisos insuficientes", 4)
        if response.status_code == 404:
            raise SkillError("objeto no encontrado", 5)
        if response.status_code >= 400:
            raise SkillError(f"error ADO {response.status_code}: {response.text[:200]}", 1)
        if not response.text:
            return {}
        return response.json()

    def work_item_get(self, item_id: int) -> dict[str, Any]:
        return self._request("GET", f"wit/workitems/{item_id}")

    def work_item_search(self, query: str = "", wiql: str = "", max_results: int = 100) -> dict[str, Any]:
        if wiql:
            found = self._request("POST", "wit/wiql", {"query": wiql}).get("workItems", [])
            ids = [i["id"] for i in found[:max_results]]
            if not ids:
                return {"count": 0, "value": []}
            return self._request("GET", f"wit/workitems?ids={','.join(map(str, ids))}&$expand=all")
        safe_query = query.replace("'", "''")
        wiql_query = (
            "SELECT [System.Id] FROM WorkItems "
            f"WHERE [System.TeamProject] = '{self.project}' AND [System.Title] CONTAINS '{safe_query}'"
        )
        return self.work_item_search(wiql=wiql_query, max_results=max_results)

    def work_item_create(self, item_type: str, title: str, dry_run: bool) -> dict[str, Any]:
        patch = [{"op": "add", "path": "/fields/System.Title", "value": title}]
        if dry_run:
            return {"dry_run": True, "request": patch, "type": item_type}
        return self._request("POST", f"wit/workitems/${item_type}", patch)

    def work_item_update(self, item_id: int, field: str, value: str, dry_run: bool) -> dict[str, Any]:
        patch = [{"op": "add", "path": f"/fields/{field}", "value": value}]
        if dry_run:
            return {"dry_run": True, "request": patch, "id": item_id}
        return self._request("PATCH", f"wit/workitems/{item_id}", patch)

    def work_item_delete(self, item_id: int, dry_run: bool) -> dict[str, Any]:
        if dry_run:
            return {"dry_run": True, "id": item_id}
        return self._request("DELETE", f"wit/workitems/{item_id}")

    def wiki_list(self) -> dict[str, Any]:
        return self._request("GET", "wiki/wikis")

    def wiki_get(self, path: str) -> dict[str, Any]:
        safe_path = path.replace(" ", "%20")
        return self._request("GET", f"wiki/wikis/{self.project}.wiki/pages?path=/{safe_path}&includeContent=true")

    def repo_list(self) -> dict[str, Any]:
        return self._request("GET", "git/repositories")

    def repo_get_file(self, repository: str, path: str, branch: str = "main") -> dict[str, Any]:
        safe_path = quote(path, safe="")
        safe_branch = quote(branch)
        return self._request(
            "GET",
            f"git/repositories/{repository}/items?path={safe_path}&includeContent=true&versionDescriptor.version={safe_branch}",
        )

    def pull_request_list(self, status: str = "active", top: int = 20) -> dict[str, Any]:
        return self._request("GET", f"git/pullrequests?searchCriteria.status={status}&$top={top}")

    def commit_list(self, repository: str, branch: str = "main", top: int = 20) -> dict[str, Any]:
        safe_branch = quote(branch)
        return self._request(
            "GET",
            f"git/repositories/{repository}/commits?searchCriteria.itemVersion.version={safe_branch}&$top={top}",
        )

    def wiql_query(self, wiql: str, top: int = 100) -> dict[str, Any]:
        found = self._request("POST", "wit/wiql", {"query": wiql}).get("workItems", [])
        ids = [i["id"] for i in found[:top]]
        if not ids:
            return {"count": 0, "ids": [], "items": []}
        details = self._request("GET", f"wit/workitems?ids={','.join(map(str, ids))}&$expand=all")
        return {
            "count": details.get("count", 0),
            "ids": ids,
            "items": details.get("value", []),
            "wiql": wiql,
        }
