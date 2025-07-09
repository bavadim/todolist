"""Data source indexer using Qdrant."""
from __future__ import annotations

import os
from typing import Iterable, Dict, Any

from qdrant_client import QdrantClient
from qdrant_client.http.models import PointStruct


DEFAULT_COLLECTION = "sources"


def index_documents(documents: Iterable[Dict[str, Any]], collection_name: str = DEFAULT_COLLECTION) -> None:
    """Index a list of documents in Qdrant.

    Each document must be a dict with ``embedding`` and ``payload`` keys.
    ``embedding`` should be a list[float] and ``payload`` any serialisable data.
    """
    client = QdrantClient(url=os.getenv("QDRANT_URL", "http://localhost:6333"))

    points = [
        PointStruct(id=i, vector=doc["embedding"], payload=doc.get("payload"))
        for i, doc in enumerate(documents)
    ]

    if points:
        client.upsert(collection_name=collection_name, points=points)


if __name__ == "__main__":
    # Example usage: indexing dummy data. Replace with real fetch from Notion/GDrive.
    dummy_docs = [
        {"embedding": [0.0, 0.1, 0.2], "payload": {"name": "example"}},
    ]
    index_documents(dummy_docs)
