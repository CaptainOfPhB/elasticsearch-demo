"""Tiny helpers shared by demos."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def load_ndjson_operations(path: Path) -> list[dict[str, Any]]:
    lines = [ln for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return [json.loads(ln) for ln in lines]


def recreate_index(es, index: str, *, settings: dict | None = None, mappings: dict | None = None) -> None:
    if es.indices.exists(index=index):
        es.indices.delete(index=index)
        print(f"deleted index: {index}")
    kwargs: dict[str, Any] = {"index": index}
    if settings is not None:
        kwargs["settings"] = settings
    if mappings is not None:
        kwargs["mappings"] = mappings
    es.indices.create(**kwargs)
    print(f"created index: {index}")


def bulk_index(es, operations: list[dict[str, Any]]) -> None:
    resp = es.bulk(operations=operations, refresh=True)
    if resp.get("errors"):
        for item in resp["items"]:
            action = next(iter(item.values()))
            if "error" in action:
                print(json.dumps(action, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(f"bulk indexed {len(resp['items'])} docs")
