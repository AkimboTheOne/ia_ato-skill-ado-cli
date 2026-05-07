from ato_skill_ado_cli.core.config import load_config


def test_load_config_defaults():
    cfg = load_config("config.example.yaml")
    assert cfg.azure_devops.api_version == "7.1"
    assert cfg.defaults.output == "md"

