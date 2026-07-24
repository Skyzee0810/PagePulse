from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from app.api.routes import router
from app.core.exceptions import (
    AuditConnectionError,
    AuditTimeoutError,
)
from app.core.logging import configure_logging
from app.middleware.request_id import (
    RequestIDMiddleware,
)

configure_logging()

app = FastAPI(
    title="Page Pulse",
    description="Production-grade URL audit service",
    version="1.0.0",
)


app.add_middleware(RequestIDMiddleware)


@app.exception_handler(AuditTimeoutError)
async def timeout_handler(
    request: Request,
    exc: AuditTimeoutError,
):
    return JSONResponse(
        status_code=504,
        content={
            "error": {
                "code": "AUDIT_TIMEOUT",
                "message": str(exc),
                "request_id": request.state.request_id,
            }
        },
    )


@app.exception_handler(AuditConnectionError)
async def connection_handler(
    request: Request,
    exc: AuditConnectionError,
):
    return JSONResponse(
        status_code=502,
        content={
            "error": {
                "code": "AUDIT_CONNECTION_ERROR",
                "message": str(exc),
                "request_id": request.state.request_id,
            }
        },
    )


app.include_router(router)


@app.get(
    "/",
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def home():
    template_path = Path(__file__).parent / "templates" / "home.html"

    return template_path.read_text(encoding="utf-8")
