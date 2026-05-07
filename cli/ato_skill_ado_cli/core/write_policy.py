from .errors import SkillError
from .models import AppConfig


def enforce_write_policy(
    config: AppConfig,
    object_type: str,
    write: bool,
    dry_run: bool,
    yes: bool,
    bulk: bool = False,
) -> None:
    policy = config.write_policy
    if object_type in policy.forbidden_objects:
        raise SkillError(f"write bloqueado para objeto: {object_type}", exit_code=7)
    if bulk and not policy.allow_bulk:
        raise SkillError("bulk write no permitido en v0.1", exit_code=7)
    if policy.require_write_flag and not write:
        raise SkillError("operación write requiere --write", exit_code=7)
    if policy.require_dry_run and not dry_run and not yes:
        raise SkillError("primera ejecución write requiere --dry-run o confirmación explícita", exit_code=7)

