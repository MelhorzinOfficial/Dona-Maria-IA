"""
API v1 Router.

Main router that aggregates all v1 endpoints.
"""

from fastapi import APIRouter


api_router = APIRouter()


@api_router.get("/status", tags=["Status"])
async def api_status() -> dict[str, str]:
    """API v1 status endpoint."""
    return {"status": "operational", "api_version": "v1"}
