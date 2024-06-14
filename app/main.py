import asyncio
import os
from pathlib import Path

from fastapi import FastAPI

from app.logger import logger
from app.models import init
from app.connect_to_db import get_engine_and_session, get_environment_db_variables
from app.routers.texts import TextsRouter
from app.routers.documents import DocumentsRouter
from app.routers.courses import CoursesRouter
from app.routers.competencies import CompetenciesRouter
from app.routers.interface import InterfaceRouter


app = FastAPI(
    title='RPD Helper',
    version='0.1.0',
    openapi_tags=[
        {
            "name": "texts",
            "description": "Contains CRUD methods for Texts entity",
        },
        {
            "name": "documents",
            "description": "Contains CRUD methods for Documents entity",
        },
        {
            "name": "courses",
            "description": "Contains CRUD methods for Courses entity",
        },
        {
            "name": "competencies",
            "description": "Contains CRUD methods for Competencies entity",
        },
        {
            "name": "interface",
            "description": "Contains project interfaces methods",
        },
    ],
)

app.include_router(TextsRouter)
app.include_router(DocumentsRouter)
app.include_router(CoursesRouter)
app.include_router(CompetenciesRouter)
app.include_router(InterfaceRouter)


async def init_app():

    env = get_environment_db_variables(Path('app', '.env'))

    connect_tasks = [
        asyncio.wait_for(asyncio.create_task(get_engine_and_session(env=env)), timeout=20),
    ]

    try:
        await asyncio.gather(*connect_tasks)
    except asyncio.TimeoutError:
        logger.critical("Timeout for databases connection, aborting")
        exit(0)

    init_tasks = [
        asyncio.wait_for(asyncio.create_task(init()), timeout=20),
    ]

    try:
        await asyncio.gather(*init_tasks)
    except asyncio.TimeoutError:
        logger.critical("Timeout for databases initialization, aborting")
        exit(0)


try:
    loop = asyncio.get_running_loop()
except RuntimeError:
    loop = asyncio.get_event_loop()

loop.create_task(init_app())
