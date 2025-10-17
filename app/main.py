from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings, get_allowed_origins
from app.db.session import engine
from app.db.models.base import Base
from app.api.routes import api_router
from app.services.scheduler import SchedulerService
from app.services.message_pipeline import plan_messages, generate_pending_messages, auto_approve_messages, send_approved_messages
from app.core.bootstrap import seed_event_types
from app.db.migrate import run_migrations


@asynccontextmanager
async def lifespan(_: FastAPI):
    # Create tables on startup for SQLite demo convenience
    Base.metadata.create_all(bind=engine)
    # Run migrations to update schema
    try:
        run_migrations()
    except Exception as e:
        print(f"Migration warning: {e}")
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

# Start background scheduler with Phase 4 pipeline
_scheduler = SchedulerService()
_scheduler.start()
_scheduler.schedule_every_cron("0 0 * * *", plan_messages)  # daily at midnight
_scheduler.schedule_every_cron("*/5 * * * *", generate_pending_messages)  # every 5 min
_scheduler.schedule_every_cron("*/5 * * * *", auto_approve_messages)  # every 5 min
_scheduler.schedule_every_cron("*/5 * * * *", send_approved_messages)  # every 5 min

