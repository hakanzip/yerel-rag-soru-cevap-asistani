"""Bulunan parçaları bağlam olarak alır, Foundry Local (phi-3.5-mini) ile cevap üretir."""
from foundry_local import FoundryLocalManager
from openai import OpenAI

from common import FOUNDRY_CHAT_ALIAS

SYSTEM_PROMPT = (
    "Sen bir soru-cevap asistanısın. SADECE aşağıda verilen bağlamı kullanarak cevap ver. "
    "Bağlamda cevap yoksa uydurma, açıkça 'Bu konuda dokümanlarda bilgi bulamadım.' de."
)

_manager = None
_client = None


def _get_client():
    global _manager, _client
    if _client is None:
        _manager = FoundryLocalManager(FOUNDRY_CHAT_ALIAS)
        _client = OpenAI(base_url=_manager.endpoint, api_key=_manager.api_key)
    return _client, _manager


def generate_answer(question: str, chunks: list[dict]) -> str:
    client, manager = _get_client()
    model_id = manager.get_model_info(FOUNDRY_CHAT_ALIAS).id

    context = "\n\n".join(f"[{c['source']}] {c['text']}" for c in chunks)
    user_prompt = f"Bağlam:\n{context}\n\nSoru: {question}"

    response = client.chat.completions.create(
        model=model_id,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
    )
    return response.choices[0].message.content
