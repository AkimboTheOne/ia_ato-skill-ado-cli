from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

from .models import AppConfig


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config(config_path: str = "config.yaml") -> AppConfig:
    load_dotenv(".env", override=False)
    file_data = _load_yaml(Path(config_path))
    cfg = AppConfig.model_validate(file_data) if file_data else AppConfig()

    ado = cfg.azure_devops
    defaults = cfg.defaults
    policy = cfg.write_policy

    ado.organization = os.getenv("ADO_ORGANIZATION", ado.organization)
    ado.project = os.getenv("ADO_PROJECT", ado.project)
    ado.api_version = os.getenv("ADO_API_VERSION", ado.api_version)
    defaults.output = os.getenv("ADO_DEFAULT_OUTPUT", defaults.output)
    defaults.workspace_dir = os.getenv("ADO_WORKSPACE_DIR", defaults.workspace_dir)
    defaults.export_dir = os.getenv("ADO_EXPORT_DIR", defaults.export_dir)
    defaults.log_dir = os.getenv("ADO_LOG_DIR", defaults.log_dir)
    defaults.tmp_dir = os.getenv("ADO_TMP_DIR", defaults.tmp_dir)
    defaults.timeout_seconds = int(os.getenv("ADO_TIMEOUT_SECONDS", defaults.timeout_seconds))
    defaults.max_results = int(os.getenv("ADO_MAX_RESULTS", defaults.max_results))
    defaults.cache_ttl_seconds = int(os.getenv("ADO_CACHE_TTL_SECONDS", defaults.cache_ttl_seconds))
    policy.enabled = os.getenv("ADO_WRITE_ENABLED", str(policy.enabled)).lower() == "true"
    policy.require_dry_run = os.getenv("ADO_REQUIRE_DRY_RUN", str(policy.require_dry_run)).lower() == "true"
    return cfg


def get_pat(config: AppConfig) -> str:
    return os.getenv(config.azure_devops.auth.pat_env_var, "")
