"""Ortak sabitler ve yardımcı fonksiyonlar: chunking, embedding, kosinüs benzerliği."""
import re
import sqlite3

DB_PATH = "knowledge.db"
FOUNDRY_CHAT_ALIAS = "phi-3.5-mini"
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

_embedder = None


def get_embedder():
    """sentence-transformers modelini tembel (lazy) yükler ve önbelleğe alır."""
    global _embedder
    if _embedder is None:
        from sentence_transformers import SentenceTransformer
        _embedder = SentenceTransformer(EMBEDDING_MODEL_NAME)
    return _embedder


def embed_text(text: str) -> list[float]:
    return get_embedder().encode(text, normalize_embeddings=True).tolist()


def chunk_text(text: str) -> list[str]:
    """Metni boş satırlara göre paragraflara böler, çok kısa parçaları eler."""
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paragraphs if len(p.strip()) > 20]


def cosine_similarity(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(y * y for y in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(DB_PATH)
