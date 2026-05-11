from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import AsyncSessionLocal, init_models
from app.core.exception_handler import (
    DOMAIN_EXCEPTIONS,
    domain_exception_handler,
    unhandled_exception_handler,
)
from app.routers.auth import router as auth_router
from app.routers.avaliacoes import router as avaliacoes_router
from app.routers.medicos import router as medicos_router
from app.routers.pacientes import router as pacientes_router
from app.routers.sintomas import router as sintomas_router
from app.seed import seed_sintomas_if_empty


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncGenerator[None, None]:
    await init_models()
    async with AsyncSessionLocal() as session:
        await seed_sintomas_if_empty(session)
    yield


app = FastAPI(lifespan=lifespan)

for domain_exception in DOMAIN_EXCEPTIONS:
    app.add_exception_handler(domain_exception, domain_exception_handler)

app.add_exception_handler(Exception, unhandled_exception_handler)

app.include_router(auth_router, prefix="/api")
app.include_router(medicos_router, prefix="/api")
app.include_router(pacientes_router, prefix="/api")
app.include_router(sintomas_router, prefix="/api")
app.include_router(avaliacoes_router, prefix="/api")
