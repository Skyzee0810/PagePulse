import time

from app.services.cache_service import (
    CacheService,
)


def test_cache_returns_stored_value():
    cache = CacheService(ttl_seconds=60)

    cache.set(
        "example.com",
        {"status_code": 200},
    )

    result = cache.get("example.com")

    assert result == {
        "status_code": 200,
    }


def test_cache_expires():
    cache = CacheService(ttl_seconds=1)

    cache.set(
        "example.com",
        {"status_code": 200},
    )

    time.sleep(1.1)

    result = cache.get("example.com")

    assert result is None
