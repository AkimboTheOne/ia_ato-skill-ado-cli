from pathlib import Path

from ato_skill_ado_cli.core.cache import get_or_set


def test_get_or_set_hits_cache_within_ttl(tmp_path: Path):
    calls = {"n": 0}

    def producer():
        calls["n"] += 1
        return {"value": 1}

    first = get_or_set(tmp_path, "k1", 60, producer)
    second = get_or_set(tmp_path, "k1", 60, producer)

    assert first["cache_hit"] is False
    assert second["cache_hit"] is True
    assert calls["n"] == 1
