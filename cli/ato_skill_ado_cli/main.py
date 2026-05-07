from __future__ import annotations

import json
from pathlib import Path

import typer

from . import __version__
from .core.ado_client import AzureDevOpsClient
from .core.cache import get_or_set
from .core.config import get_pat, load_config
from .core.errors import SkillError
from .core.render import render_markdown, render_markdown_custom, write_manifest
from .core.security import mask_secret
from .core.write_policy import enforce_write_policy

app = typer.Typer(help="Azure DevOps Cloud CLI skill (@ado)")
work_item_app = typer.Typer()
wiki_app = typer.Typer()
repo_app = typer.Typer()
pr_app = typer.Typer()
commit_app = typer.Typer()
bundle_app = typer.Typer()
service_app = typer.Typer()
config_app = typer.Typer()
app.add_typer(work_item_app, name="work-item")
app.add_typer(wiki_app, name="wiki")
app.add_typer(repo_app, name="repo")
app.add_typer(pr_app, name="pr")
app.add_typer(commit_app, name="commit")
app.add_typer(bundle_app, name="bundle")
app.add_typer(service_app, name="service")
app.add_typer(config_app, name="config")


def _echo(data, as_json: bool = False):
    if as_json:
        typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        if isinstance(data, (dict, list)):
            typer.echo(json.dumps(data, indent=2, ensure_ascii=False))
        else:
            typer.echo(data)


def _render(template: str, data: dict, custom_template: str = "") -> str:
    if custom_template:
        return render_markdown_custom(custom_template, data)
    return render_markdown(template, data)


def _read_cached(cfg, key: str, producer):
    cache_dir = Path(cfg.defaults.workspace_dir) / "cache"
    return get_or_set(cache_dir, key, cfg.defaults.cache_ttl_seconds, producer)


@app.command()
def version():
    _echo(__version__)


@app.command()
def init():
    _echo("baseline v0.1 inicializado")


@config_app.command("init")
def config_init():
    if not Path("config.yaml").exists():
        Path("config.yaml").write_text(Path("config.example.yaml").read_text(encoding="utf-8"), encoding="utf-8")
    _echo("config.yaml listo")


@app.command()
def context(json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    data = {
        "skill": "ato-skill-ado-cli",
        "version": __version__,
        "baseline_mode": "Baseline B",
        "organization": cfg.azure_devops.organization,
        "project": cfg.azure_devops.project,
        "commands": ["doctor", "validate", "context", "capabilities", "work-item", "wiki", "repo", "pr", "commit", "bundle", "run"],
        "workspace_dir": cfg.defaults.workspace_dir,
        "export_dir": cfg.defaults.export_dir,
        "cache_ttl_seconds": cfg.defaults.cache_ttl_seconds,
    }
    _echo(data, json_out)


@app.command()
def capabilities(json_out: bool = typer.Option(False, "--json")):
    data = {
        "read": [
            "work-item.search",
            "work-item.get",
            "work-item.wiql",
            "wiki.list",
            "wiki.get",
            "repo.list",
            "repo.get-file",
            "pr.list",
            "commit.list",
        ],
        "export": ["work-item.export", "wiki.export", "repo.export", "pr.export", "commit.export", "bundle.export"],
        "write": ["work-item.create", "work-item.update", "work-item.delete"],
        "forbidden": ["wiki.write", "repo.write", "bulk.write"],
        "p2_contracts": ["run", "validate"],
    }
    _echo(data, json_out)


@app.command()
def usage():
    _echo("Usa @ado o comandos directos: ato-skill-ado-cli work-item search --query OAuth")


@app.command()
def examples():
    _echo("Ejemplos en ./examples/")


@app.command()
def schema(json_out: bool = typer.Option(False, "--json")):
    schemas = [p.name for p in Path("contracts").glob("*.json")]
    _echo({"schemas": schemas}, json_out)


@app.command()
def logs():
    _echo("logs/ado/")


@app.command()
def doctor(ci: bool = False, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    pat = get_pat(cfg)
    data = {
        "organization_set": bool(cfg.azure_devops.organization),
        "project_set": bool(cfg.azure_devops.project),
        "pat_set": bool(pat),
        "pat_masked": mask_secret(pat),
        "api_version": cfg.azure_devops.api_version,
        "cache_ttl_seconds": cfg.defaults.cache_ttl_seconds,
        "ci_mode": ci,
    }
    ok = all([data["organization_set"], data["project_set"], data["pat_set"]])
    data["status"] = "ok" if ok else "error"
    _echo(data, json_out)
    if not ok:
        raise SkillError("doctor falló por configuración incompleta", 2)


@app.command()
def validate(format: str = "text", payload_file: str = ""):
    required = ["README.md", "SKILL.md", ".env.example", "config.example.yaml", "contracts"]
    missing = [p for p in required if not Path(p).exists()]
    result = {"status": "ok" if not missing else "error", "missing": missing}
    if payload_file:
        payload = json.loads(Path(payload_file).read_text(encoding="utf-8"))
        result["payload_valid"] = bool(payload.get("operation"))
        if not result["payload_valid"]:
            result["status"] = "error"
    if format == "json":
        _echo(result, True)
    else:
        _echo(result)
    if result["status"] == "error":
        raise SkillError("estructura inválida", 6)


@app.command()
def run(payload_file: str, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    payload = json.loads(Path(payload_file).read_text(encoding="utf-8"))
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    operation = payload.get("operation", "")
    if operation == "context":
        result = {"organization": cfg.azure_devops.organization, "project": cfg.azure_devops.project}
    elif operation == "work-item.search":
        result = client.work_item_search(query=payload.get("query", ""), wiql=payload.get("wiql", ""), max_results=payload.get("top", cfg.defaults.max_results))
    elif operation == "wiql.query":
        result = client.wiql_query(payload.get("wiql", ""), top=payload.get("top", cfg.defaults.max_results))
    else:
        raise SkillError(f"operation no soportada en run: {operation}", 6)
    _echo({"operation": operation, "result": result}, json_out)


@app.command()
def ask(prompt: str):
    text = prompt.lower()
    if "work item" in text or "workitem" in text:
        _echo("Sugerencia: ato-skill-ado-cli work-item search --query \"...\"")
        return
    if "wiki" in text:
        _echo("Sugerencia: ato-skill-ado-cli wiki export --path \"Architecture\"")
        return
    _echo("Necesito organización/proyecto configurado o explícito, tipo de objeto y criterio de búsqueda.")


@work_item_app.command("search")
def wi_search(query: str = "", wiql: str = "", json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    key = f"wi.search:{query}:{wiql}:{cfg.defaults.max_results}"
    cached = _read_cached(cfg, key, lambda: client.work_item_search(query=query, wiql=wiql, max_results=cfg.defaults.max_results))
    _echo(cached, json_out)


@work_item_app.command("wiql")
def wi_wiql(query: str, top: int = 100, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    key = f"wi.wiql:{query}:{top}"
    cached = _read_cached(cfg, key, lambda: client.wiql_query(query, top=top))
    _echo(cached, json_out)


@work_item_app.command("get")
def wi_get(id: int, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).work_item_get(id)
    _echo(data, json_out)


@work_item_app.command("export")
def wi_export(id: int, out: str, template: str = "", manifest_json: bool = True):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    wi = client.work_item_get(id)
    fields = wi.get("fields", {})
    doc = _render("markdown/work-item.md.j2", {
        "id": id,
        "title": fields.get("System.Title", ""),
        "type": fields.get("System.WorkItemType", ""),
        "state": fields.get("System.State", ""),
        "assigned_to": (fields.get("System.AssignedTo") or {}).get("displayName", ""),
        "area_path": fields.get("System.AreaPath", ""),
        "iteration_path": fields.get("System.IterationPath", ""),
        "tags": fields.get("System.Tags", ""),
        "description": fields.get("System.Description", ""),
        "acceptance_criteria": fields.get("Microsoft.VSTS.Common.AcceptanceCriteria", ""),
        "relations": wi.get("relations", []),
        "organization": cfg.azure_devops.organization,
        "project": cfg.azure_devops.project,
        "exported_at": "",
        "manifest_path": "manifest.json",
    }, template)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "work-item.md"
    md_path.write_text(doc, encoding="utf-8")
    manifest = {"operation": "export", "object_type": "work_item", "object_id": str(id), "output_files": [str(md_path)]}
    if manifest_json:
        write_manifest(out_dir / "manifest.json", manifest)
    _echo({"status": "ok", "out": str(out_dir)})


@work_item_app.command("create")
def wi_create(type: str, title: str, write: bool = False, dry_run: bool = False, yes: bool = False, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    enforce_write_policy(cfg, "work_item", write, dry_run, yes)
    data = AzureDevOpsClient(cfg, get_pat(cfg)).work_item_create(type, title, dry_run=dry_run and not yes)
    _echo(data, json_out)


@work_item_app.command("update")
def wi_update(id: int, field: str, value: str, write: bool = False, dry_run: bool = False, yes: bool = False, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    enforce_write_policy(cfg, "work_item", write, dry_run, yes)
    data = AzureDevOpsClient(cfg, get_pat(cfg)).work_item_update(id, field, value, dry_run=dry_run and not yes)
    _echo(data, json_out)


@work_item_app.command("delete")
def wi_delete(id: int, write: bool = False, dry_run: bool = False, yes: bool = False, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    enforce_write_policy(cfg, "work_item", write, dry_run, yes)
    data = AzureDevOpsClient(cfg, get_pat(cfg)).work_item_delete(id, dry_run=dry_run and not yes)
    _echo(data, json_out)


@wiki_app.command("list")
def wiki_list(json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).wiki_list()
    _echo(data, json_out)


@wiki_app.command("get")
def wiki_get(path: str, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).wiki_get(path)
    _echo(data, json_out)


@wiki_app.command("export")
def wiki_export(path: str, out: str, template: str = ""):
    cfg = load_config()
    page = AzureDevOpsClient(cfg, get_pat(cfg)).wiki_get(path)
    content = page.get("content", "")
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "wiki-page.md"
    md_path.write_text(
        _render("markdown/wiki-page.md.j2", {"path": path, "content": content, "organization": cfg.azure_devops.organization, "project": cfg.azure_devops.project}, template),
        encoding="utf-8",
    )
    write_manifest(out_dir / "manifest.json", {"operation": "export", "object_type": "wiki_page", "object_id": path, "output_files": [str(md_path)]})
    _echo({"status": "ok", "out": str(out_dir)})


@repo_app.command("list")
def repo_list(json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    key = "repo.list"
    cached = _read_cached(cfg, key, client.repo_list)
    _echo(cached, json_out)


@repo_app.command("get-file")
def repo_get_file(repository: str, path: str, branch: str = "main", json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    key = f"repo.get-file:{repository}:{path}:{branch}"
    cached = _read_cached(cfg, key, lambda: client.repo_get_file(repository, path, branch))
    _echo(cached, json_out)


@repo_app.command("export")
def repo_export(repository: str, path: str, out: str, branch: str = "main"):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).repo_get_file(repository, path, branch)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "repo-file.md"
    md_path.write_text(f"# Repo file\n\n- repository: {repository}\n- path: {path}\n- branch: {branch}\n\n```\n{data.get('content', '')}\n```\n", encoding="utf-8")
    write_manifest(out_dir / "manifest.json", {"operation": "export", "object_type": "repo_file", "object_id": f"{repository}:{path}", "output_files": [str(md_path)]})
    _echo({"status": "ok", "out": str(out_dir)})


@pr_app.command("list")
def pr_list(status: str = "active", top: int = 20, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    key = f"pr.list:{status}:{top}"
    cached = _read_cached(cfg, key, lambda: client.pull_request_list(status, top))
    _echo(cached, json_out)


@pr_app.command("export")
def pr_export(out: str, status: str = "active", top: int = 20):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).pull_request_list(status, top)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "pull-requests.md"
    lines = ["# Pull Requests", ""]
    for item in data.get("value", []):
        lines.append(f"- {item.get('pullRequestId')}: {item.get('title', '')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    write_manifest(out_dir / "manifest.json", {"operation": "export", "object_type": "pull_requests", "object_id": status, "output_files": [str(md_path)]})
    _echo({"status": "ok", "out": str(out_dir)})


@commit_app.command("list")
def commit_list(repository: str, branch: str = "main", top: int = 20, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    key = f"commit.list:{repository}:{branch}:{top}"
    cached = _read_cached(cfg, key, lambda: client.commit_list(repository, branch, top))
    _echo(cached, json_out)


@commit_app.command("export")
def commit_export(repository: str, out: str, branch: str = "main", top: int = 20):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).commit_list(repository, branch, top)
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "commits.md"
    lines = ["# Commits", ""]
    for item in data.get("value", []):
        lines.append(f"- {item.get('commitId', '')[:8]} {item.get('comment', '')}")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    write_manifest(out_dir / "manifest.json", {"operation": "export", "object_type": "commits", "object_id": repository, "output_files": [str(md_path)]})
    _echo({"status": "ok", "out": str(out_dir)})


@bundle_app.command("export")
def bundle_export(out: str, query: str = "", wiki_path: str = "Architecture", pr_status: str = "active"):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)

    work_items = client.work_item_search(query=query, max_results=cfg.defaults.max_results)
    wiki = client.wiki_get(wiki_path)
    repos = client.repo_list()
    prs = client.pull_request_list(pr_status, 20)
    first_repo = (repos.get("value") or [{}])[0]
    commits = client.commit_list(first_repo.get("id", ""), "main", 20) if first_repo.get("id") else {"count": 0, "value": []}

    bundle = {
        "work_items": work_items,
        "wiki": wiki,
        "repos": repos,
        "pull_requests": prs,
        "commits": commits,
    }
    bundle_path = out_dir / "bundle.json"
    bundle_path.write_text(json.dumps(bundle, ensure_ascii=False, indent=2), encoding="utf-8")
    write_manifest(out_dir / "manifest.json", {"operation": "export", "object_type": "bundle", "object_id": "context", "output_files": [str(bundle_path)]})
    _echo({"status": "ok", "out": str(out_dir)})


@service_app.command("list")
def service_list():
    _echo({"services": ["azure-devops"]})


@service_app.command("doctor")
def service_doctor(name: str = "azure-devops", json_out: bool = typer.Option(False, "--json")):
    _echo({"service": name, "status": "ok"}, json_out)


@service_app.command("config")
def service_config_init(name: str = "azure-devops"):
    _echo(f"usa services/{name}/{name}.config.example.yaml")


def run_cli():
    try:
        app()
    except SkillError as e:
        typer.echo(str(e))
        raise typer.Exit(code=e.exit_code)


def run():
    run_cli()


if __name__ == "__main__":
    run_cli()
