"""Soruyu embed eder, SQLite'taki tüm parçalarla kosinüs benzerliği hesaplar,
en iyi parçaları döndürür."""
import json

from local_rag_qa.common import cosine_similarity, embed_text, get_connection


def retrieve(question: str, top_k: int = 3) -> list[dict]:
    conn = get_connection()
    rows = conn.execute("SELECT source, text, embedding FROM chunks").fetchall()
    conn.close()

    if not rows:
        return []

    query_vector = embed_text(question)

    scored = []
    for source, text, embedding_json in rows:
        vector = json.loads(embedding_json)
        score = cosine_similarity(query_vector, vector)
        scored.append({"source": source, "text": text, "score": score})

    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored[:top_k]


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "Bileşik faiz nedir?"
    for r in retrieve(question):
        print(f"[{r['score']:.3f}] {r['source']}: {r['text'][:80]}...")
