# 담당: C (인프라 + 챗봇)
from fastapi import APIRouter,Request
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()

@router.post("", response_model=ChatResponse)
def chat(req: ChatRequest, request: Request):
    # 프록시(nginx 등) 뒤에 있다면 X-Forwarded-For 우선 확인
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        ip = forwarded.split(",")[0].strip()
    else:
        # request 객체에서 직접 클라이언트 IP 추출 (없을 경우를 대비해 예외 처리 보완)
        ip = request.client.host if request.client else "127.0.0.1"
    result = chat_service.ask(ip, req.message)
    return ChatResponse(**result)



