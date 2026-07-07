# Yerel RAG Soru-Cevap Asistanı

## Amaç
Küçük bir doküman kümesi üzerinde, internet bağlantısı olmadan, yerelde çalışan bir dil modeli kullanarak soru cevaplayan bir Q&A asistanı. Model uydurmaz: önce kullanıcının dokümanlarından ilgili parçayı bulur (retrieval), sonra sadece bu parçalara dayanarak cevap verir (generation). Bilgi dokümanlarda yoksa asistan bunu açıkça belirtir.

## Nasıl çalışır (RAG akışı)
1. **Ingest** — `docs/` içindeki dokümanlar paragraflara bölünür, her paragraf bir embedding vektörüne çevrilir ve metniyle birlikte SQLite'a yazılır.
2. **Retrieve** — Kullanıcının sorusu da embed edilir; SQLite'taki tüm parça vektörleriyle kosinüs benzerliği hesaplanır ve en yakın 3 parça seçilir.
3. **Generate** — Seçilen parçalar bağlam olarak sistem promptuna eklenir ("SADECE bu bağlamı kullan, bilmiyorsan bilmediğini söyle") ve Foundry Local üzerinde yerelde çalışan `phi-3.5-mini` modeline gönderilir.
4. **CLI** — `main.py`, kullanıcıdan soru alıp bu üç adımı çalıştıran ve cevabı ekrana basan bir terminal döngüsüdür (`quit` ile çıkılır).

## Kullanılan Microsoft aracı: Foundry Local
Cevap üretimi (generation) adımı tamamen **Foundry Local** üzerinden, yerelde çalışan `phi-3.5-mini` modeliyle yapılır. Foundry Local, Apple Silicon'da Metal ile GPU hızlandırması kullanan, OpenAI uyumlu bir yerel REST endpoint açar; bu projede `foundry-local-sdk` ile bu endpoint'e bağlanılıp standart `openai` Python SDK'sı üzerinden sohbet isteği gönderilir.

### Not: embedding adımı hakkında kapsam sapması
Planda embedding için Foundry Local'in `qwen3-embedding-0.6b` modeli kullanılması öngörülmüştü. Kurulum sırasında **Foundry Local'in güncel model kataloğunda hiçbir embedding modeli bulunmadığı** tespit edildi (`foundry model list --filter task=embedding` boş sonuç döndürüyor). Bu nedenle embedding adımı için, tamamen yerelde çalışan açık kaynaklı `sentence-transformers` (`all-MiniLM-L6-v2`, ~90 MB) kullanıldı. Bu değişiklik projenin "internet olmadan yerelde çalışma" hedefini bozmaz; yalnızca ilk model indirmesi internet gerektirir.

## Kurulum
```bash
# 1) Foundry Local (Homebrew ile)
brew tap microsoft/foundrylocal
brew trust --tap microsoft/foundrylocal   # resmi Microsoft deposu olduğu doğrulandıktan sonra
brew install foundrylocal

# 2) Servisi başlat
foundry service start

# 3) phi-3.5-mini modelini indir
foundry model download phi-3.5-mini

# 4) Python ortamı
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```
> Not: `foundry-local-sdk`, Python 3.9'da kullanılamayan `X | None` tip söz dizimini kullanıyor. Python 3.10 altındaysanız `eval_type_backport` paketi (requirements.txt'de mevcut) bunu otomatik düzeltir.

## Çalıştırma
```bash
source .venv/bin/activate
python3 ingest.py     # docs/ içeriğini embed edip knowledge.db'ye yazar (bir kere çalıştırılır)
python3 main.py        # soru-cevap döngüsünü başlatır
```

## Dosya yapısı
```
proje1-yerel-rag/
├── docs/            # 6 küçük .md finans dokümanı (bilgi tabanı)
├── common.py        # chunking, embedding, kosinüs benzerliği yardımcıları
├── ingest.py         # docs/ → chunk → embed → SQLite
├── retrieve.py       # soru → embed → en yakın parçaları bul
├── generate.py       # parçalar + soru → Foundry Local (phi-3.5-mini) → cevap
├── main.py            # CLI döngüsü
├── knowledge.db       # (otomatik oluşur, ingest.py ile)
├── requirements.txt
└── README.md
```

## Sınırlamalar / gelecek fikirler
- Chunking basitçe boş satıra göre paragraf bölme; daha gelişmiş (token bazlı, örtüşmeli) chunking eklenebilir.
- Embedding adımı Foundry Local yerine sentence-transformers kullanıyor; Foundry Local kataloğuna embedding modeli eklenirse geçiş yapılabilir.
- Şu an sadece CLI arayüz var; Streamlit/HTML arayüz, çoklu dil desteği ve kaynak alıntısı süslemeleri kapsam dışı bırakıldı.
- Değerlendirme (ölçüm) katmanı yok; doğruluk manuel test ile kontrol edildi.
