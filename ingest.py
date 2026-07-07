"""docs/ klasöründeki dokümanları paragraflara böler, embed eder ve SQLite'a yazar."""
import json
import os

from common import DB_PATH, chunk_text, embed_text, get_connection

DOCS_DIR = "docs"


def init_db(conn):
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            text TEXT NOT NULL,
            embedding TEXT NOT NULL
        )
        """
    )
    conn.commit()


def ingest():
    conn = get_connection()
    init_db(conn)
    conn.execute("DELETE FROM chunks")

    total = 0
    for filename in sorted(os.listdir(DOCS_DIR)):
        if not filename.endswith((".md", ".txt")):
            continue
        path = os.path.join(DOCS_DIR, filename)
        with open(path, encoding="utf-8") as f:
            raw = f.read()

        for chunk in chunk_text(raw):
            vector = embed_text(chunk)
            conn.execute(
                "INSERT INTO chunks (source, text, embedding) VALUES (?, ?, ?)",
                (filename, chunk, json.dumps(vector)),
            )
            total += 1

    conn.commit()
    conn.close()
    print(f"{total} parça {DB_PATH} içine yazıldı.")


if __name__ == "__main__":
    ingest()
