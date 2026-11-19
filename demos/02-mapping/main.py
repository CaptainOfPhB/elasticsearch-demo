"""02-mapping: text vs keyword (simple)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from shared.bulk_util import recreate_index  # noqa: E402
from shared.es_client import get_client, wait_until_ready  # noqa: E402

INDEX = "mapping_demo"


def main() -> None:
    es = get_client()
    wait_until_ready(es)

    recreate_index(
        es,
        INDEX,
        mappings={
            "properties": {
                "title": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "brand": {"type": "keyword"},
                "price": {"type": "float"},
            }
        },
    )

    es.index(
        index=INDEX,
        id="1",
        document={"title": "机械键盘 Pro", "brand": "KeyChron", "price": 799},
        refresh=True,
    )

    match_hits = es.search(index=INDEX, query={"match": {"title": "键盘"}})
    term_brand = es.search(index=INDEX, query={"term": {"brand": "KeyChron"}})
    term_title_wrong = es.search(index=INDEX, query={"term": {"title": "机械键盘 Pro"}})
    term_title_ok = es.search(index=INDEX, query={"term": {"title.keyword": "机械键盘 Pro"}})

    print("match title~键盘:", match_hits["hits"]["total"]["value"])
    print("term brand=KeyChron:", term_brand["hits"]["total"]["value"])
    print("term title (wrong):", term_title_wrong["hits"]["total"]["value"])
    print("term title.keyword:", term_title_ok["hits"]["total"]["value"])
    print("done. see demos/02-mapping/console.http")


if __name__ == "__main__":
    main()
