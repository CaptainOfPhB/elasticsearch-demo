"""01-crud: create index, index/get/update/delete docs, bulk load sample data."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from shared.es_client import get_client, wait_until_ready  # noqa: E402

INDEX = "products"
DATA_FILE = ROOT / "data" / "products.ndjson"

SETTINGS = {
    "number_of_shards": 1,
    "number_of_replicas": 0,
}

MAPPINGS = {
    "properties": {
        "name": {"type": "text", "fields": {"keyword": {"type": "keyword"}}},
        "brand": {"type": "keyword"},
        "category": {"type": "keyword"},
        "price": {"type": "float"},
        "tags": {"type": "keyword"},
        "in_stock": {"type": "boolean"},
        "sold": {"type": "integer"},
        "created_at": {"type": "date"},
        "description": {"type": "text"},
    }
}


def recreate_index(es) -> None:
    if es.indices.exists(index=INDEX):
        es.indices.delete(index=INDEX)
        print(f"deleted index: {INDEX}")
    es.indices.create(index=INDEX, settings=SETTINGS, mappings=MAPPINGS)
    print(f"created index: {INDEX}")


def bulk_load(es) -> None:
    lines = [
        ln for ln in DATA_FILE.read_text(encoding="utf-8").splitlines() if ln.strip()
    ]
    operations = [json.loads(ln) for ln in lines]
    resp = es.bulk(operations=operations, refresh=True)
    if resp.get("errors"):
        print("bulk had errors:")
        for item in resp["items"]:
            action = next(iter(item.values()))
            if "error" in action:
                print(json.dumps(action, ensure_ascii=False, indent=2))
        raise SystemExit(1)
    print(f"bulk indexed {len(resp['items'])} docs from {DATA_FILE.name}")


def demo_single_doc_ops(es) -> None:
    doc = {
        "name": "临时测试商品",
        "brand": "DemoBrand",
        "category": "测试",
        "price": 1.0,
        "tags": ["demo"],
        "in_stock": True,
        "sold": 0,
        "created_at": "2024-01-01T00:00:00Z",
        "description": "用于演示单条 CRUD，稍后会删除",
    }
    es.index(index=INDEX, id="tmp-1", document=doc, refresh=True)
    got = es.get(index=INDEX, id="tmp-1")
    print("get tmp-1:", got["_source"]["name"], got["_source"]["price"])

    es.update(index=INDEX, id="tmp-1", doc={"price": 9.9}, refresh=True)
    got = es.get(index=INDEX, id="tmp-1")
    print("after update price:", got["_source"]["price"])

    es.delete(index=INDEX, id="tmp-1", refresh=True)
    print("deleted tmp-1")


def search_all(es) -> None:
    resp = es.search(index=INDEX, query={"match_all": {}}, size=20)
    total = resp["hits"]["total"]["value"]
    print(f"match_all total={total}")
    for hit in resp["hits"]["hits"]:
        src = hit["_source"]
        print(f"  - {hit['_id']}: {src['name']} / {src['brand']} / ¥{src['price']}")


def main() -> None:
    es = get_client()
    wait_until_ready(es)
    recreate_index(es)
    bulk_load(es)
    demo_single_doc_ops(es)
    search_all(es)
    print("done. open Kibana Dev Tools and try demos/01-crud/console.http")


if __name__ == "__main__":
    main()
