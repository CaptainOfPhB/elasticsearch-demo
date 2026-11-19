"""05-bm25: compare default BM25 vs tuned k1/b."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from shared.bulk_util import recreate_index  # noqa: E402
from shared.es_client import get_client, wait_until_ready  # noqa: E402

DOCS = {
    "short": {
        "title": "机械键盘",
        "content": "机械键盘好用",
    },
    "medium": {
        "title": "机械键盘选购",
        "content": "机械键盘适合编程。机械键盘有青轴茶轴红轴。选购机械键盘要看配列。",
    },
    "long": {
        "title": "机械键盘长文",
        "content": (
            "机械键盘是常见外设。很多人讨论机械键盘手感。机械键盘轴体分青轴茶轴红轴。"
            "办公室里机械键盘声响要留意。旅行时可带紧凑机械键盘。"
            "总之机械键盘话题很多，但核心仍是手感与配列。"
        ),
    },
}


def index_body(k1: float, b: float) -> tuple[dict, dict]:
    settings = {
        "number_of_shards": 1,
        "number_of_replicas": 0,
        "similarity": {
            "custom_bm25": {
                "type": "BM25",
                "k1": k1,
                "b": b,
            }
        },
    }
    mappings = {
        "properties": {
            "title": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                "similarity": "custom_bm25",
            },
            "content": {
                "type": "text",
                "analyzer": "ik_max_word",
                "search_analyzer": "ik_smart",
                "similarity": "custom_bm25",
            },
        }
    }
    return settings, mappings


def seed(es, index: str) -> None:
    for doc_id, body in DOCS.items():
        es.index(index=index, id=doc_id, document=body)
    es.indices.refresh(index=index)


def rank(es, index: str, query: str) -> list[tuple[str, float]]:
    resp = es.search(index=index, query={"match": {"content": query}})
    return [(h["_id"], float(h["_score"])) for h in resp["hits"]["hits"]]


def main() -> None:
    es = get_client()
    wait_until_ready(es)

    s1, m1 = index_body(1.2, 0.75)
    s2, m2 = index_body(2.0, 0.0)
    recreate_index(es, "bm25_default", settings=s1, mappings=m1)
    recreate_index(es, "bm25_tuned", settings=s2, mappings=m2)
    seed(es, "bm25_default")
    seed(es, "bm25_tuned")

    q = "机械键盘"
    print("default BM25 k1=1.2 b=0.75:", rank(es, "bm25_default", q))
    print("tuned   BM25 k1=2.0 b=0.0 :", rank(es, "bm25_tuned", q))

    explained = es.explain(index="bm25_default", id="long", query={"match": {"content": q}})
    print("explain long matched:", explained.get("matched"))
    print("explain long score:", explained.get("explanation", {}).get("value"))
    print("done. see demos/05-bm25/console.http")
    print("tip: b=0 时长文不再因长度被强烈压分；k1 更大时重复词加分更明显")


if __name__ == "__main__":
    main()
