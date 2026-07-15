from openai import OpenAI
from app.core.config import settings
from app.services.chat_context_store import chat_context_store


class ChatService:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def ask(self, ip: str, user_message: str) -> str:
        history = chat_context_store.get_history(ip)

        messages = [{"role": "system", "content": settings.CHAT_SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        response = self._client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=messages,
        )
        answer = response.choices[0].message.content

        # 대화 기록 갱신 (DB 저장 X, 메모리만)
        chat_context_store.append(ip, "user", user_message)
        chat_context_store.append(ip, "assistant", answer)

        return answer

    def reset(self, ip: str) -> None:
        chat_context_store.clear(ip)


chat_service = ChatService()