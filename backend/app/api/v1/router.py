"""
API v1 Router.

Main router that aggregates all v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1.auth import router as auth_router

api_router = APIRouter()

# Include auth router
api_router.include_router(auth_router)


@api_router.get("/status", tags=["Status"])
async def api_status() -> dict[str, str]:
    """API v1 status endpoint."""
    return {"status": "operational", "api_version": "v1"}
