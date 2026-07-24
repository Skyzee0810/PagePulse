from pydantic import BaseModel, HttpUrl


class AuditRequest(BaseModel):
    url: HttpUrl


class AuditResponse(BaseModel):
    request_id: str
    url: str
    status_code: int
    response_time_ms: float
    is_cached: bool
