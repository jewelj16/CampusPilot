from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.mess import router as mess_router
from app.core.config import get_settings
from app.core.exceptions import ConflictError, NotFoundError, ValidationError
from app.seed import seed
from app.core.db import get_engine, Base
from sqlalchemy.orm import Session
from app.repositories.orm_models import StudentORM # ensure models are registered

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    engine = get_engine()
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        seed(session)
        session.commit()
    yield


app = FastAPI(
    title=settings.app_name,
    description=(
        "CampusPilot Phase 1 API — mess registration only. "
        "Runs on an in-memory dummy backend; no database yet."
    ),
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---- typed-exception -> HTTP mapping ---------------------------------
# A single place that turns service-layer errors into responses, so API
# routes stay free of try/except (see Section 10 of the plan).
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


@app.exception_handler(ConflictError)
async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return JSONResponse(status_code=409, content={"detail": str(exc)})


@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return JSONResponse(status_code=400, content={"detail": str(exc)})


@app.get("/health", tags=["health"])
def health() -> dict:
    return {"status": "ok", "env": settings.app_env}


app.include_router(mess_router, prefix=settings.api_v1_prefix)
