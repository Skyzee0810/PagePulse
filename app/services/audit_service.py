import asyncio
import time

import httpx

from app.core.config import settings
from app.core.exceptions import (
    AuditConnectionError,
    AuditTimeoutError,
)
from app.services.cache_service import CacheService


class AuditService:
    def __init__(self):
        self.semaphore = asyncio.Semaphore(
            settings.max_concurrent_requests
        )

        self.cache = CacheService(
            settings.cache_ttl_seconds
        )

    async def audit_url(self, url: str) -> dict:
        cached_result = self.cache.get(url)

        if cached_result:
            return {
                **cached_result,
                "is_cached": True,
            }

        async with self.semaphore:
            result = await self._perform_audit(url)

        self.cache.set(url, result)

        return {
            **result,
            "is_cached": False,
        }

    async def _perform_audit(self, url: str) -> dict:
        start_time = time.perf_counter()

        timeout = httpx.Timeout(
            settings.request_timeout_seconds
        )

        try:
            async with httpx.AsyncClient(
                timeout=timeout,
                follow_redirects=True,
            ) as client:
                response = await client.get(url)

        except httpx.TimeoutException as exc:
            raise AuditTimeoutError(
                "The target URL timed out"
            ) from exc

        except httpx.RequestError as exc:
            raise AuditConnectionError(
                "Unable to connect to the target URL"
            ) from exc

        end_time = time.perf_counter()

        response_time_ms = round(
            (end_time - start_time) * 1000,
            2,
        )

        return {
            "url": url,
            "status_code": response.status_code,
            "response_time_ms": response_time_ms,
        }