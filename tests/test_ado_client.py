from ato_skill_ado_cli.core.ado_client import AzureDevOpsClient
from ato_skill_ado_cli.core.models import AppConfig


class DummyResponse:
    def __init__(self, status_code=200, payload=None, text=""):
        self.status_code = status_code
        self._payload = payload or {}
        self.text = text or "{}"

    def json(self):
        return self._payload


class DummySession:
    def __init__(self):
        self.calls = []
        self.auth = None

    def request(self, method, url, json=None, timeout=None):
        self.calls.append({"method": method, "url": url, "json": json, "timeout": timeout})
        if method == "POST" and "wit/wiql" in url:
            return DummyResponse(payload={"workItems": [{"id": 101}]})
        if method == "GET" and "wit/workitems?" in url:
            return DummyResponse(payload={"count": 1, "value": [{"id": 101}]})
        return DummyResponse(payload={})


def build_client():
    cfg = AppConfig()
    cfg.azure_devops.organization = "org"
    cfg.azure_devops.project = "proj"
    cfg.azure_devops.api_version = "7.1"
    client = AzureDevOpsClient(cfg, "pat")
    client.session = DummySession()
    return client


def test_url_adds_api_version_with_ampersand_when_path_has_query():
    client = build_client()
    url = client._url("wit/workitems?ids=1&$expand=all")
    assert url.endswith("wit/workitems?ids=1&$expand=all&api-version=7.1")


def test_work_item_search_escapes_quotes_in_query():
    client = build_client()
    client.work_item_search(query="O'Hara")
    wiql_call = client.session.calls[0]
    assert wiql_call["method"] == "POST"
    assert "O''Hara" in wiql_call["json"]["query"]


def test_work_item_search_with_wiql_builds_valid_workitems_url():
    client = build_client()
    result = client.work_item_search(wiql="SELECT [System.Id] FROM WorkItems")
    get_call = client.session.calls[1]
    assert get_call["method"] == "GET"
    assert "wit/workitems?ids=101&$expand=all&api-version=7.1" in get_call["url"]
    assert result["count"] == 1
