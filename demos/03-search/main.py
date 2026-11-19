"""03-search: match / term / range / bool (simple)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from shared.es_client import get_client, wait_until_ready  # noqa: E402

INDEX = "products"


def show(label: str, resp) -> None:
    total = resp["hits"]["total"]["value"]
    names = [h["_source"]["name"] for h in resp["hits"]["hits"]]
    print(f"{label}: total={total} -> {names}")


def main() -> None:
    es = get_client()
    wait_until_ready(es)
    if not es.indices.exists(index=INDEX):
        raise SystemExit(f"index {INDEX} missing; run: python demos/01-crud/main.py")

    show("match description~办公", es.search(index=INDEX, query={"match": {"description": "办公"}}))
    show("term brand=KeyChron", es.search(index=INDEX, query={"term": {"brand": "KeyChron"}}))
    show(
        "range price 200-800",
        es.search(index=INDEX, query={"range": {"price": {"gte": 200, "lte": 800}}}),
    )
    show(
        "bool must+filter",
        es.search(
            index=INDEX,
            query={
                "bool": {
                    "must": [{"match": {"description": "办公"}}],
                    "filter": [
                        {"term": {"in_stock": True}},
                        {"range": {"price": {"lte": 1000}}},
                    ],
                    "must_not": [{"term": {"category": "家具"}}],
                }
            },
        ),
    )
    print("done. see demos/03-search/console.http")


if __name__ == "__main__":
    main()
