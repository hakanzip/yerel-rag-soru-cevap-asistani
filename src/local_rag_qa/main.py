"""CLI döngüsü: soru al, ilgili parçaları bul, cevap üret, yazdır. 'quit' ile çık."""
from local_rag_qa.generate import generate_answer
from local_rag_qa.retrieve import retrieve


def main():
    print("Yerel RAG Soru-Cevap Asistanı (çıkmak için 'quit' yaz)\n")
    while True:
        question = input("Soru: ").strip()
        if not question:
            continue
        if question.lower() in ("quit", "exit"):
            break

        chunks = retrieve(question)
        if not chunks:
            print("Cevap: Bu konuda dokümanlarda bilgi bulamadım.\n")
            continue

        answer = generate_answer(question, chunks)
        print(f"Cevap: {answer}")
        print(f"  (kaynaklar: {', '.join(sorted({c['source'] for c in chunks}))})\n")


if __name__ == "__main__":
    main()
