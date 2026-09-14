"""Command-line entry point: ``local-rag-qa ingest`` / ``local-rag-qa ask``.

Imports for each subcommand are deferred into the branch that needs them, so
``local-rag-qa --help`` never has to import sentence-transformers, openai or
foundry-local-sdk just to print usage.
"""
import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="local-rag-qa",
        description="A small, fully local retrieval-augmented Q&A CLI.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    subparsers.add_parser("ingest", help="Embed everything in docs/ into knowledge.db")
    subparsers.add_parser("ask", help="Start the interactive Q&A loop")

    args = parser.parse_args()

    if args.command == "ingest":
        from local_rag_qa.ingest import ingest
        ingest()
    elif args.command == "ask":
        from local_rag_qa.main import main as ask_loop
        ask_loop()


if __name__ == "__main__":
    main()
