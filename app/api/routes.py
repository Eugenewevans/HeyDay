from fastapi import APIRouter

from app.api.customers import router as customers_router
from app.api.templates import router as templates_router


api_router = APIRouter(prefix="/api")


@api_router.get("/health")
def health():
    return {"ok": True}


api_router.include_router(customers_router)
api_router.include_router(templates_router)

