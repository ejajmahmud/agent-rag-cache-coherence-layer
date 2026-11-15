"""Automated test suite for RAG Cache Coherence Layer."""
import unittest
from agent_rag_cache_coherence_layer.core import RAGCacheCoherenceLayer

class TestRAGCacheCoherenceLayer(unittest.TestCase):
    def test_cache_hit_and_stale_invalidation(self):
        cache = RAGCacheCoherenceLayer()
        cache.set("explain code", "it handles auth", {"auth.py": "abc"})

        # Coherent hit
        self.assertEqual(cache.get("explain code", {"auth.py": "abc"}), "it handles auth")

        # Incoherent miss and eviction
        self.assertIsNone(cache.get("explain code", {"auth.py": "def"}))
        # Subsequent check with old hash must also be miss (evicted)
        self.assertIsNone(cache.get("explain code", {"auth.py": "abc"}))
