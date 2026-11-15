"""Core implementation of RAG cache coherence layer."""
import hashlib
from typing import Dict, Optional, Any

class CacheItem:
    def __init__(self, query: str, response: str, file_hashes: Dict[str, str]):
        self.query = query
        self.response = response
        self.file_hashes = file_hashes  # path -> sha256

class RAGCacheCoherenceLayer:
    def __init__(self):
        self._cache: Dict[str, CacheItem] = {}

    def _query_key(self, query: str) -> str:
        return hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()[:16]

    def set(self, query: str, response: str, file_hashes: Dict[str, str]):
        key = self._query_key(query)
        self._cache[key] = CacheItem(query, response, file_hashes)

    def get(self, query: str, current_file_hashes: Dict[str, str]) -> Optional[str]:
        key = self._query_key(query)
        item = self._cache.get(key)
        if not item:
            return None

        # Verify coherence: all dependency hashes must match current hashes
        for path, expected_hash in item.file_hashes.items():
            if current_file_hashes.get(path) != expected_hash:
                # Cache is stale! Invalidate immediately
                del self._cache[key]
                return None

        return item.response
