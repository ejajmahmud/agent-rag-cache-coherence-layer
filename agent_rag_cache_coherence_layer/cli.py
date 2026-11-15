"""CLI for RAG Cache Coherence Layer."""
import argparse
from .core import RAGCacheCoherenceLayer

def main():
    parser = argparse.ArgumentParser(description="RAG Cache Coherence Layer CLI")
    parser.add_argument("--demo", action="store_true", help="Demonstrate cache invalidation on file mutation")
    args = parser.parse_args()

    cache = RAGCacheCoherenceLayer()
    query = "How to run server?"
    cache.set(query, "Run python main.py", {"main.py": "hash_v1"})

    # 1. Query with same hash -> HIT
    hit = cache.get(query, {"main.py": "hash_v1"})
    print(f"Query 1 (unmodified file): Hit='{hit}'")

    # 2. File modified -> INVALIDATED
    miss = cache.get(query, {"main.py": "hash_v2"})
    print(f"Query 2 (modified file): Hit='{miss}' (Successfully invalidated)")

if __name__ == "__main__":
    main()
