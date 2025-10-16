from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, get_allowed_origins
from app.db.session import engine
from app.db.models.base import Base
from app.api.routes import api_router
from app.services.scheduler import SchedulerService
from app.services.automation_runner import plan_upcoming_messages, dispatch_due_messages
from app.core.bootstrap import seed_event_types


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create tables on startup for SQLite demo convenience
    Base.metadata.create_all(bind=engine)
    seed_event_types()
    yield


app = FastAPI(title="HeyDay API", version="0.1.0", lifespan=lifespan)


@app.get("/")
def read_root():
    return {"status": "ok", "name": "HeyDay API"}


app.include_router(api_router)

# CORS for Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Start background scheduler (simple daily runner placeholder)
_scheduler = SchedulerService()
_scheduler.start()
_scheduler.schedule_every_cron("*/5 * * * *", plan_upcoming_messages)
_scheduler.schedule_every_cron("*/5 * * * *", dispatch_due_messages)

