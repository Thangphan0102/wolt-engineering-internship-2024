from fastapi import APIRouter

from app.api.routes import fees


api_router = APIRouter()
api_router.include_router(fees.router, prefix="/fees", tags=["fees"])
