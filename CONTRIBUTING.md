# Contributing to local-rag-qa

Thanks for considering a contribution. This is a small project, so the process is small too.

## Setup

```bash
git clone https://github.com/hakanzip/yerel-rag-soru-cevap-asistani.git
cd yerel-rag-soru-cevap-asistani
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

`[dev]` pulls in `pytest` and `ruff` alongside the runtime dependencies (`sentence-transformers`, `openai`, `foundry-local-sdk`) — the full install can take a few minutes the first time because of `sentence-transformers`' own dependencies.

## Before opening a PR

```bash
ruff check .
pytest -v
```

Both run in CI on every PR (Python 3.9 and 3.12), so it's faster to catch issues locally first.

## What's easy to test, what isn't

`common.py`'s `chunk_text` and `cosine_similarity` are pure functions — easy to unit test, see `tests/test_common.py` for the pattern. `ingest.py`, `retrieve.py`, and `generate.py` depend on a running [Foundry Local](https://github.com/microsoft/Foundry-Local) instance for the LLM call, so they're currently only covered by manual testing. If your change touches those, describe how you tested it manually in the PR description.

## Code style

Kept intentionally plain — small modules, no framework, few dependencies. `ruff check .` enforces the basics (unused imports, import order, a few upgrade checks). No strong opinions beyond that; match what's already there.

## Picking something to work on

Check the [open issues](https://github.com/hakanzip/yerel-rag-soru-cevap-asistani/issues), especially ones labeled `good first issue`. If you have an idea that isn't listed, open an issue first to discuss scope before writing code — saves both of us time if it turns out to be out of scope for v0.1.

## Code of Conduct

This project follows the [Contributor Covenant](CODE_OF_CONDUCT.md).
