from app.services.rate_limit_service import (
    RateLimitService,
)


def test_rate_limit_allows_requests():
    limiter = RateLimitService(
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.is_allowed(
        "client-1"
    )

    assert limiter.is_allowed(
        "client-1"
    )

def test_rate_limit_rejects_excess_requests():
    limiter = RateLimitService(
        max_requests=2,
        window_seconds=60,
    )

    assert limiter.is_allowed(
        "client-1"
    )

    assert limiter.is_allowed(
        "client-1"
    )

    assert not limiter.is_allowed(
        "client-1"
    )

def test_rate_limit_is_per_client():
    limiter = RateLimitService(
        max_requests=1,
        window_seconds=60,
    )

    assert limiter.is_allowed(
        "client-1"
    )

    assert not limiter.is_allowed(
        "client-1"
    )

    assert limiter.is_allowed(
        "client-2"
    )

