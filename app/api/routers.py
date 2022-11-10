from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoints import auth, file_manager, learner_manager, issuer_manager


def execute():
    fastAPI = FastAPI()
    origins = [
        "*",
    ]

    fastAPI.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    fastAPI.include_router(auth.router, prefix="/api")
    fastAPI.include_router(file_manager.router, prefix="/api/file")
    fastAPI.include_router(learner_manager.router, prefix="/api/learner")
    fastAPI.include_router(issuer_manager.router, prefix="/api/issuer")

    return fastAPI
