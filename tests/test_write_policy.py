import pytest

from ato_skill_ado_cli.core.errors import SkillError
from ato_skill_ado_cli.core.models import AppConfig
from ato_skill_ado_cli.core.write_policy import enforce_write_policy


def test_write_requires_flag():
    cfg = AppConfig()
    with pytest.raises(SkillError) as exc:
        enforce_write_policy(cfg, "work_item", write=False, dry_run=True, yes=False)
    assert exc.value.exit_code == 7


def test_write_forbidden_object():
    cfg = AppConfig()
    with pytest.raises(SkillError):
        enforce_write_policy(cfg, "wiki", write=True, dry_run=True, yes=False)

