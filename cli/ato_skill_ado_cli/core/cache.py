from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Any, Callable


def _cache_path(cache_dir: Path, key: str) -> Path:
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return cache_dir / f"{digest}.json"


def get_or_set(cache_dir: Path, key: str, ttl_seconds: int, producer: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    path = _cache_path(cache_dir, key)
    now = int(time.time())

    if path.exists():
        cached = json.loads(path.read_text(encoding="utf-8"))
        cached_at = int(cached.get("cached_at", 0))
        if now - cached_at <= ttl_seconds:
            return {"cache_hit": True, "data": cached.get("data", {})}

    data = producer()
    payload = {"cached_at": now, "data": data}
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"cache_hit": False, "data": data}
