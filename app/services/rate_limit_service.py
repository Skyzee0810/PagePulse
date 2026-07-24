import time


class RateLimitService:
    def __init__(
        self,
        max_requests: int,
        window_seconds: int,
    ):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._requests: dict[str, list[float]] = {}

    def is_allowed(self, client_id: str) -> bool:
        now = time.time()

        request_times = self._requests.get(
            client_id,
            [],
        )

        valid_requests = [
            timestamp
            for timestamp in request_times
            if now - timestamp < self.window_seconds
        ]

        if len(valid_requests) >= self.max_requests:
            self._requests[client_id] = valid_requests
            return False

        valid_requests.append(now)

        self._requests[client_id] = valid_requests

        return True
