import time
from typing import Any


class CacheService:
    def __init__(self, ttl_seconds: int):
        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, tuple[Any, float]] = {}

    def get(self, key: str) -> Any | None:
        cached_item = self._cache.get(key)

        if cached_item is None:
            return None

        value, expires_at = cached_item

        if time.time() >= expires_at:
            del self._cache[key]
            return None

        return value

    def set(self, key: str, value: Any) -> None:
        expires_at = time.time() + self.ttl_seconds

        self._cache[key] = (value, expires_at)