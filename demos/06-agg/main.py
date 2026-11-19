"""06-agg: terms + avg/sum (simple)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from shared.es_client import get_client, wait_until_ready  # noqa: E402

INDEX = "products"


def main() -> None:
    es = get_client()
    wait_until_ready(es)
    if not es.indices.exists(index=INDEX):
        raise SystemExit(f"index {INDEX} missing; run: python demos/01-crud/main.py")

    by_brand = es.search(index=INDEX, size=0, aggs={"by_brand": {"terms": {"field": "brand"}}})
    print("by_brand:")
    for b in by_brand["aggregations"]["by_brand"]["buckets"]:
        print(f"  {b['key']}: {b['doc_count']}")

    metrics = es.search(
        index=INDEX,
        size=0,
        aggs={
            "avg_price": {"avg": {"field": "price"}},
            "sum_sold": {"sum": {"field": "sold"}},
        },
    )
    print("avg_price:", round(metrics["aggregations"]["avg_price"]["value"], 2))
    print("sum_sold:", metrics["aggregations"]["sum_sold"]["value"])

    nested = es.search(
        index=INDEX,
        size=0,
        aggs={
            "by_category": {
                "terms": {"field": "category"},
                "aggs": {"avg_price": {"avg": {"field": "price"}}},
            }
        },
    )
    print("by_category avg_price:")
    for b in nested["aggregations"]["by_category"]["buckets"]:
        print(f"  {b['key']}: count={b['doc_count']} avg={round(b['avg_price']['value'], 2)}")
    print("done. see demos/06-agg/console.http")


if __name__ == "__main__":
    main()
