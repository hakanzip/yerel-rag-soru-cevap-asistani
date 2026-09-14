# Local RAG Q&A Assistant

[🇹🇷 Türkçe README](README.tr.md)

A small, fully local retrieval-augmented Q&A tool: no internet connection needed at query time, no data leaves your machine. Point it at a folder of documents, ask questions in natural language, and it answers *only* from what's in your documents — if the answer isn't there, it says so instead of making something up.

## How it works

1. **Ingest** — files in `docs/` are split into paragraphs, each paragraph is embedded and written to a local SQLite database.
2. **Retrieve** — your question is embedded the same way; the 3 closest chunks are found by cosine similarity.
3. **Generate** — those chunks are passed as context to a locally-running LLM (`phi-3.5-mini` via [Microsoft Foundry Local](https://github.com/microsoft/Foundry-Local)) with a strict "answer only from this context" system prompt.
4. **CLI** — `main.py` runs the ask-loop in your terminal until you type `quit`.

## Why local

Foundry Local runs `phi-3.5-mini` behind an OpenAI-compatible REST endpoint, GPU-accelerated via Metal on Apple Silicon. Nothing about a question or a document ever leaves the machine — a good fit for private notes, internal docs, or just not wanting your queries logged by someone else's API.

## Quickstart

```bash
# 1) Foundry Local (Homebrew)
brew tap microsoft/foundrylocal
brew install foundrylocal
foundry service start
foundry model download phi-3.5-mini

# 2) Python environment
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3) Index your documents, then ask
python3 ingest.py      # embeds everything in docs/ into knowledge.db
python3 main.py         # starts the Q&A loop
```

> `foundry-local-sdk` uses the `X | None` type syntax, which needs Python ≥3.10 (or the `eval_type_backport` package already in `requirements.txt` on older versions).

## Project layout

```
.
├── docs/            # your knowledge base (.md / .txt files go here)
├── common.py        # chunking, embedding, cosine-similarity helpers
├── ingest.py        # docs/ -> chunks -> embeddings -> SQLite
├── retrieve.py      # question -> embedding -> nearest chunks
├── generate.py      # chunks + question -> Foundry Local -> answer
├── main.py          # CLI loop
├── requirements.txt
└── README.md
```

## A note on scope (kept honest on purpose)

The original plan called for embedding via Foundry Local's `qwen3-embedding-0.6b`. At setup time, Foundry Local's model catalog had no embedding model available (`foundry model list --filter task=embedding` returned empty), so embedding runs on the fully local, open-source `sentence-transformers` (`all-MiniLM-L6-v2`, ~90 MB) instead. This doesn't break the "runs offline" goal — only the first model download needs internet.

## Limitations / roadmap

- Chunking is a plain blank-line paragraph split; token-aware, overlapping chunking would help.
- Embedding uses `sentence-transformers` rather than Foundry Local — revisit if/when Foundry Local ships an embedding model.
- CLI only for now; a Streamlit/HTML UI, multi-language support, and answer-with-citation formatting are out of scope for v0.1.
- No automated evaluation layer yet — correctness was checked manually.
- Packaging (a `pip install`-able CLI) and an automated test suite are in progress — see [open issues](../../issues).

## Contributing

Issues and PRs welcome — see `CONTRIBUTING.md` (coming soon) or just open an issue with what you'd like to change.

## License

[MIT](LICENSE)
