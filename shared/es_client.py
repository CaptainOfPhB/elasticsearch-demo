"""Shared Elasticsearch client for demos."""

from __future__ import annotations

import os
import time

from dotenv import load_dotenv
from elasticsearch import Elasticsearch

load_dotenv()

DEFAULT_ES_URL = "http://localhost:9200"


def get_es_url() -> str:
    return os.getenv("ES_URL", DEFAULT_ES_URL)


def get_client(url: str | None = None) -> Elasticsearch:
    return Elasticsearch(url or get_es_url())


def wait_until_ready(
    es: Elasticsearch, retries: int = 30, interval: float = 2.0
) -> None:
    for attempt in range(1, retries + 1):
        try:
            if es.ping():
                info = es.info()
                print(
                    f"Elasticsearch ready: v{info['version']['number']} ({get_es_url()})"
                )
                return
        except Exception as exc:  # noqa: BLE001 - demo script, show any connection error
            print(f"[{attempt}/{retries}] waiting for ES... ({exc})")
        time.sleep(interval)
    raise RuntimeError("Elasticsearch did not become ready in time")
