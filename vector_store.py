"""FAISS index + aligned metadata. Invariant: FAISS position i <-> records[i]."""
import json
import os

import faiss
import numpy as np

from errors import RAGError


class VectorStore:
    def __init__(self, dim: int):
        self.index = faiss.IndexFlatIP(dim)   # inner product == cosine on normalized vectors
        self.records: list[dict] = []

    def add(self, embeddings: np.ndarray, records: list[dict]) -> None:
        if len(embeddings) != len(records):
            raise RAGError("Internal error: embeddings and chunks are out of sync.")
        if embeddings.ndim != 2 or embeddings.shape[1] != self.index.d:
            raise RAGError("Embedding dimension mismatch. Was the embedding model changed?")
        try:
            self.index.add(embeddings)
        except Exception:
            raise RAGError("Could not add vectors to the search index.")
        for record in records:
            record = dict(record)
            record["chunk_id"] = len(self.records)
            self.records.append(record)

    def search(self, query_vector: np.ndarray, top_k: int = 5) -> list[dict]:
        if self.index.ntotal == 0:
            return []
        k = min(top_k, self.index.ntotal)     # k > ntotal would return -1 ids
        try:
            scores, ids = self.index.search(query_vector, k)
        except Exception:
            raise RAGError("The search index failed. Please try again.")
        results = []
        for score, idx in zip(scores[0], ids[0]):
            if idx == -1:
                continue
            item = dict(self.records[idx])
            item["score"] = float(score)
            results.append(item)
        return results

    def has_document(self, doc_hash: str) -> bool:
        return any(r.get("doc_hash") == doc_hash for r in self.records)

    def document_names(self) -> list[str]:
        return sorted({r["doc_name"] for r in self.records})

    def save(self, folder: str) -> None:
        os.makedirs(folder, exist_ok=True)
        faiss.write_index(self.index, os.path.join(folder, "index.faiss"))
        with open(os.path.join(folder, "records.json"), "w", encoding="utf-8") as f:
            json.dump(self.records, f, ensure_ascii=False)

    @classmethod
    def load(cls, folder: str) -> "VectorStore":
        index = faiss.read_index(os.path.join(folder, "index.faiss"))
        with open(os.path.join(folder, "records.json"), encoding="utf-8") as f:
            records = json.load(f)
        if index.ntotal != len(records):
            raise RAGError("Saved index and records are out of sync.")
        store = cls(index.d)
        store.index, store.records = index, records
        return store

    def __len__(self) -> int:
        return self.index.ntotal