import logging

from fastapi import (
    APIRouter,
    HTTPException,
    Request,
    status,
)

from app.core.config import settings
from app.schemas.audit_schema import (
    AuditRequest,
    AuditResponse,
)
from app.services.audit_service import AuditService
from app.services.rate_limit_service import (
    RateLimitService,
)

rate_limit_service = RateLimitService(
    max_requests=settings.rate_limit_requests,
    window_seconds=settings.rate_limit_window_seconds,
)



logger = logging.getLogger(__name__)

router = APIRouter()

audit_service = AuditService()


# @router.post(
#     "/audit",
#     response_model=AuditResponse,
# )
# async def audit_url(
#     request: Request,
#     audit_request: AuditRequest,
# ):
#     client_id = request.client.host

#     if not rate_limit_service.is_allowed(
#         client_id
#     ):
#         raise HTTPException(
#             status_code=status.HTTP_429_TOO_MANY_REQUESTS,
#             detail={
#                 "code": "RATE_LIMIT_EXCEEDED",
#                 "message": (
#                     "Too many requests. "
#                     "Please try again later."
#                 ),
#                 "request_id": request.state.request_id,
#             },
#         )

#     request_id = request.state.request_id

#     result = await audit_service.audit_url(
#         str(audit_request.url)
#     )

#     return AuditResponse(
#         request_id=request_id,
#         url=result["url"],
#         status_code=result["status_code"],
#         response_time_ms=result["response_time_ms"],
#         is_cached=result["is_cached"],
#     )


@router.post(
    "/audit",
    response_model=AuditResponse,
)
async def audit_url(
    request: Request,
    audit_request: AuditRequest,
):
    client_id = request.client.host
    
    if not rate_limit_service.is_allowed(
        client_id
    ):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail={
                "code": "RATE_LIMIT_EXCEEDED",
                "message": (
                    "Too many requests. "
                    "Please try again later."
                ),
                "request_id": request.state.request_id,
            },
        )
    
    request_id = request.state.request_id
    url = str(audit_request.url)

    logger.info(
        "audit_started",
        extra={
            "request_id": request_id,
            "url": url,
        },
    )

    result = await audit_service.audit_url(url)

    logger.info(
        "audit_completed",
        extra={
            "request_id": request_id,
            "url": url,
        },
    )

    return AuditResponse(
        request_id=request_id,
        url=result["url"],
        status_code=result["status_code"],
        response_time_ms=result["response_time_ms"],
        is_cached=result["is_cached"],
    )