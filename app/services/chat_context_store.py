import threading
import time
from typing import Optional
from app.core.config import settings


class ChatContextStore:
    """
    IP를 key로 하는 인메모리 대화 컨텍스트 저장소.
    Thread-safe 싱글톤. DB를 사용하지 않고 프로세스 메모리에만 저장한다.
    """
    _instance: Optional["ChatContextStore"] = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._init_store()
        return cls._instance

    def _init_store(self):
        # ip -> {"messages": [...], "updated_at": float}
        self._store: dict[str, dict] = {}
        self._store_lock = threading.Lock()

    def get_history(self, ip: str) -> list[dict]:
        with self._store_lock:
            entry = self._store.get(ip)
            return list(entry["messages"]) if entry else []

    def append(self, ip: str, role: str, content: str) -> None:
        with self._store_lock:
            entry = self._store.setdefault(ip, {"messages": [], "updated_at": time.time()})
            entry["messages"].append({"role": role, "content": content})
            entry["updated_at"] = time.time()

            # 오래된 메시지 정리 (system 프롬프트는 여기 저장 안 하므로 단순 slicing)
            max_len = settings.CHAT_MAX_HISTORY
            if len(entry["messages"]) > max_len:
                entry["messages"] = entry["messages"][-max_len:]

    def clear(self, ip: str) -> None:
        with self._store_lock:
            self._store.pop(ip, None)


# 모듈 레벨 싱글톤 인스턴스
chat_context_store = ChatContextStore()