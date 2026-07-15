import json
from openai import OpenAI, RateLimitError, AuthenticationError, APIError
from fastapi import HTTPException
from app.core.config import settings
from app.core.prompts.busan_travel_prompt import BUSAN_TRAVEL_SYSTEM_PROMPT
from app.services.chat_context_store import chat_context_store


class ChatService:
    def __init__(self):
        self._client = OpenAI(api_key=settings.OPENAI_API_KEY)

    def ask(self, ip: str, user_message: str) -> dict:
        history = chat_context_store.get_history(ip)

        messages = [{"role": "system", "content": BUSAN_TRAVEL_SYSTEM_PROMPT}]
        messages.extend(history)
        messages.append({"role": "user", "content": user_message})

        try:
            response = self._client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=messages,
                response_format={"type": "json_object"},  # JSON 형식 강제
            )
        except RateLimitError as e:
            raise HTTPException(status_code=503, detail="AI 서비스 사용량 한도를 초과했습니다.") from e
        except AuthenticationError as e:
            raise HTTPException(status_code=500, detail="AI 서비스 인증 오류입니다.") from e
        except APIError as e:
            raise HTTPException(status_code=502, detail="AI 서비스 응답 중 오류가 발생했습니다.") from e

        raw_content = response.choices[0].message.content

        try:
            parsed = json.loads(raw_content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=502, detail="AI 응답을 해석할 수 없습니다.")

        reply_text = parsed.get("reply", "")
        recommended = parsed.get("recommendedPlaces", [])

        # 대화 기록은 reply 텍스트만 저장 (JSON 전체를 저장하면 다음 프롬프트가 오염됨)
        chat_context_store.append(ip, "user", user_message)
        chat_context_store.append(ip, "assistant", reply_text)

        return {"reply": reply_text, "recommendedPlaces": recommended}

    def reset(self, ip: str) -> None:
        chat_context_store.clear(ip)


chat_service = ChatService()