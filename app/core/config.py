from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Page Pulse"
    environment: str = "development"

    request_timeout_seconds: float = 10.0
    cache_ttl_seconds: int = 300

    rate_limit_requests: int = 10
    rate_limit_window_seconds: int = 60

    max_concurrent_requests: int = 10

    class ConfigDict:
        env_file = ".env"
        case_sensitive = False


settings = Settings()