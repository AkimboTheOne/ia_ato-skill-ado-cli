from __future__ import annotations

import json
from pathlib import Path

import typer
from pydantic import BaseModel

from . import __version__
from .core.config import get_pat, load_config
from .core.errors import SkillError
from .core.render import render_markdown, write_manifest
from .core.security import mask_secret
from .core.write_policy import enforce_write_policy
from .core.ado_client import AzureDevOpsClient

app = typer.Typer(help="Azure DevOps Cloud CLI skill (@ado)")
work_item_app = typer.Typer()
wiki_app = typer.Typer()
service_app = typer.Typer()
config_app = typer.Typer()
app.add_typer(work_item_app, name="work-item")
app.add_typer(wiki_app, name="wiki")
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
        "commands": ["doctor", "validate", "context", "capabilities", "work-item", "wiki"],
        "workspace_dir": cfg.defaults.workspace_dir,
        "export_dir": cfg.defaults.export_dir,
    }
    _echo(data, json_out)


@app.command()
def capabilities(json_out: bool = typer.Option(False, "--json")):
    data = {
        "read": ["work-item.search", "work-item.get", "wiki.list", "wiki.get"],
        "export": ["work-item.export", "wiki.export"],
        "write": ["work-item.create", "work-item.update", "work-item.delete"],
        "forbidden": ["wiki.write", "repo.write", "bulk.write"],
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
        "ci_mode": ci,
    }
    ok = all([data["organization_set"], data["project_set"], data["pat_set"]])
    data["status"] = "ok" if ok else "error"
    _echo(data, json_out)
    if not ok:
        raise SkillError("doctor falló por configuración incompleta", 2)


@app.command()
def validate(format: str = "text"):
    required = ["README.md", "SKILL.md", ".env.example", "config.example.yaml", "contracts"]
    missing = [p for p in required if not Path(p).exists()]
    result = {"status": "ok" if not missing else "error", "missing": missing}
    if format == "json":
        _echo(result, True)
    else:
        _echo(result)
    if missing:
        raise SkillError("estructura inválida", 6)


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
    data = AzureDevOpsClient(cfg, get_pat(cfg)).work_item_search(query=query, wiql=wiql, max_results=cfg.defaults.max_results)
    _echo(data, json_out)


@work_item_app.command("get")
def wi_get(id: int, json_out: bool = typer.Option(False, "--json")):
    cfg = load_config()
    data = AzureDevOpsClient(cfg, get_pat(cfg)).work_item_get(id)
    _echo(data, json_out)


@work_item_app.command("export")
def wi_export(id: int, out: str, manifest_json: bool = True):
    cfg = load_config()
    client = AzureDevOpsClient(cfg, get_pat(cfg))
    wi = client.work_item_get(id)
    fields = wi.get("fields", {})
    doc = render_markdown("markdown/work-item.md.j2", {
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
    })
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
def wiki_export(path: str, out: str):
    cfg = load_config()
    page = AzureDevOpsClient(cfg, get_pat(cfg)).wiki_get(path)
    content = page.get("content", "")
    out_dir = Path(out)
    out_dir.mkdir(parents=True, exist_ok=True)
    md_path = out_dir / "wiki-page.md"
    md_path.write_text(
        render_markdown("markdown/wiki-page.md.j2", {"path": path, "content": content, "organization": cfg.azure_devops.organization, "project": cfg.azure_devops.project}),
        encoding="utf-8",
    )
    write_manifest(out_dir / "manifest.json", {"operation": "export", "object_type": "wiki_page", "object_id": path, "output_files": [str(md_path)]})
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


def run():
    try:
        app()
    except SkillError as e:
        typer.echo(str(e))
        raise typer.Exit(code=e.exit_code)


if __name__ == "__main__":
    run()

