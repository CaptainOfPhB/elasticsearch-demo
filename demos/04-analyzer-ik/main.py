"""04-analyzer-ik: IK tokenize + Chinese search."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from shared.bulk_util import bulk_index, load_ndjson_operations, recreate_index  # noqa: E402
from shared.es_client import get_client, wait_until_ready  # noqa: E402

INDEX = "articles"
DATA = ROOT / "data" / "articles.ndjson"
TEXT = "机械键盘适合编程办公"

SETTINGS = {"number_of_shards": 1, "number_of_replicas": 0}
MAPPINGS = {
    "properties": {
        "title": {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_smart",
        },
        "content": {
            "type": "text",
            "analyzer": "ik_max_word",
            "search_analyzer": "ik_smart",
        },
        "category": {"type": "keyword"},
        "tags": {"type": "keyword"},
    }
}


def tokens(es, analyzer: str) -> list[str]:
    resp = es.indices.analyze(analyzer=analyzer, text=TEXT)
    return [t["token"] for t in resp["tokens"]]


def main() -> None:
    es = get_client()
    wait_until_ready(es)

    plugins = es.cat.plugins(format="json")
    names = {p.get("component") for p in plugins}
    if "analysis-ik" not in names:
        raise SystemExit(
            "analysis-ik not installed; rebuild image: docker compose build elasticsearch"
        )

    print("standard :", tokens(es, "standard"))
    print("ik_smart :", tokens(es, "ik_smart"))
    print("ik_max   :", tokens(es, "ik_max_word"))

    recreate_index(es, INDEX, settings=SETTINGS, mappings=MAPPINGS)
    bulk_index(es, load_ndjson_operations(DATA))

    resp = es.search(
        index=INDEX,
        query={"match": {"content": "机械键盘"}},
        highlight={"fields": {"content": {}}},
    )
    print(f"search 机械键盘: total={resp['hits']['total']['value']}")
    for hit in resp["hits"]["hits"]:
        print(f"  - {hit['_source']['title']}  score={hit['_score']:.4f}")
        if "highlight" in hit:
            print("    hl:", hit["highlight"].get("content"))
    print("done. see demos/04-analyzer-ik/console.http")


if __name__ == "__main__":
    main()
