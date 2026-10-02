"""Wrapper around the embedding model. Swap the model by changing the name only."""
import numpy as np
from sentence_transformers import SentenceTransformer

from errors import RAGError


class Embedder:
    def __init__(self, model_name: str):
        self.model_name = model_name
        try:
            self.model = SentenceTransformer(model_name)
        except Exception:
            raise RAGError(f"Could not load the embedding model '{model_name}'. Check the name and your internet connection.")
        self.dim = self.model.get_sentence_embedding_dimension()

    def embed(self, texts: list[str], batch_size: int = 32) -> np.ndarray:
        """Return an L2-normalized float32 matrix of shape (n, dim)."""
        if not texts:
            raise RAGError("There is no text to embed.")
        try:
            vectors = self.model.encode(
                texts, batch_size=batch_size, normalize_embeddings=True,
                convert_to_numpy=True, show_progress_bar=False,
            )
        except Exception:
            raise RAGError("Embedding generation failed. Please try again.")
        return vectors.astype("float32")

    def embed_query(self, query: str) -> np.ndarray:
        # Note: some models (e.g. BGE) expect an instruction prefix for queries. MiniLM does not.
        return self.embed([query])