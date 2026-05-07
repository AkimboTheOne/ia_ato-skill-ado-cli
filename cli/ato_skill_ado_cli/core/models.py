from pydantic import BaseModel, Field


class AzureDevOpsAuth(BaseModel):
    pat_env_var: str = "ADO_PAT"


class AzureDevOpsConfig(BaseModel):
    organization: str = ""
    project: str = ""
    api_version: str = "7.1"
    auth: AzureDevOpsAuth = Field(default_factory=AzureDevOpsAuth)


class DefaultsConfig(BaseModel):
    output: str = "md"
    workspace_dir: str = "workspace/ado"
    export_dir: str = "exports/ado"
    log_dir: str = "logs/ado"
    tmp_dir: str = "tmp/ado"
    max_results: int = 100
    timeout_seconds: int = 30
    cache_ttl_seconds: int = 300


class WritePolicy(BaseModel):
    enabled: bool = False
    require_write_flag: bool = True
    require_dry_run: bool = True
    require_confirmation: bool = True
    allowed_objects: list[str] = ["work_item"]
    forbidden_objects: list[str] = ["wiki", "repo", "pull_request", "pipeline"]
    allow_bulk: bool = False


class AppConfig(BaseModel):
    azure_devops: AzureDevOpsConfig = Field(default_factory=AzureDevOpsConfig)
    defaults: DefaultsConfig = Field(default_factory=DefaultsConfig)
    write_policy: WritePolicy = Field(default_factory=WritePolicy)
