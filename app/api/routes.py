from fastapi import APIRouter

from app.api.customers import router as customers_router
from app.api.templates import router as templates_router
from app.api.datasets import router as datasets_router
from app.api.event_types import router as event_types_router
from app.api.automations import router as automations_router
from app.api.messages import router as messages_router
from app.api.consents import router as consents_router


api_router = APIRouter(prefix="/api")


@api_router.get("/health")
def health():
    return {"ok": True}


api_router.include_router(customers_router)
api_router.include_router(templates_router)
api_router.include_router(datasets_router)
api_router.include_router(event_types_router)
api_router.include_router(automations_router)
api_router.include_router(messages_router)
api_router.include_router(consents_router)

