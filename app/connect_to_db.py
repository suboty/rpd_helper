import os
import asyncio
from asyncio import current_task
from functools import lru_cache
from typing import Dict, Optional

from dotenv import dotenv_values
from pydantic import error_wrappers, BaseSettings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_scoped_session
from sqlalchemy.orm import sessionmaker

from app.logger import logger
from app.settings import settings


class ConfigLoadDotenvError(Exception):
    pass


class ConfigVariablesError(Exception):
    pass


class ConfigDatabaseConnectionError(Exception):
    pass


@lru_cache
def load_env(env) -> Dict:
    config = {}
    if env:
        if os.path.isfile(env):
            env_dict = dict(dotenv_values(env))
            for key in env_dict.keys():
                config[key] = env_dict[key]
            return config
        else:
            logger.critical('Critical error! Invalid env`s path')
            raise ConfigLoadDotenvError('Invalid env`s path')
    else:
        logger.critical('Critical error! No path to env')
        raise ConfigLoadDotenvError('No path to env')


class EnvironmentDBSettings(BaseSettings):
    DATABASE_DIALECT: str
    DATABASE_HOSTNAME: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_SCHEMA: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DEBUG_MODE: bool


@lru_cache
def get_environment_db_variables(path_to_db_env):
    try:
        return EnvironmentDBSettings(**load_env(path_to_db_env))
    except error_wrappers.ValidationError as e:
        logger.critical('Critical error! Error with load values from envs: {e}')
        raise ConfigVariablesError(f'Error with load values from envs: {e}')


async def connect_to_database(env):
    try:
        DATABASE_URL = f"{env.DATABASE_DIALECT}://{env.DATABASE_USERNAME}:{env.DATABASE_PASSWORD}" \
                       f"@{env.DATABASE_HOSTNAME}:{env.DATABASE_PORT}/{env.DATABASE_NAME}"

        Engine = create_async_engine(
            DATABASE_URL,
            echo=env.DEBUG_MODE,
            pool_pre_ping=True,
            pool_size=20,
            max_overflow=0
        )

        SessionLocal = async_scoped_session(
            sessionmaker(bind=Engine, expire_on_commit=False, class_=AsyncSession),
            scopefunc=current_task)

        connection = await SessionLocal.connection()
        await connection.execution_options(schema_translate_map={None: env.DATABASE_SCHEMA})

        return Engine, SessionLocal

    except Exception as e:
        logger.critical(f'Error while creating engine for DB {env.DATABASE_NAME}! '
                        f'Exception: {e}')
        raise ConfigDatabaseConnectionError(f'Error while creating engine for DB {env.DATABASE_NAME}! '
                                            f'Exception: {e}')


async def get_engine_and_session(env, is_need_return=False):
    try:
        event_loop = asyncio.get_running_loop()

        Engine, SessionLocal = await event_loop.create_task(connect_to_database(env))

        settings.set_setting(name='Engine', value=Engine)
        settings.set_setting(name='SessionLocal', value=SessionLocal)

        logger.info('Connection to database is created')

        if is_need_return:
            return Engine, SessionLocal

    except Exception as e:
        logger.critical(f'Error while creating engine for DB {env.DATABASE_NAME}! '
                        f'Exception: {e}')
        raise ConfigDatabaseConnectionError(f'Error while creating engine for DB {env.DATABASE_NAME}! '
                                            f'Exception: {e}')


async def get_db_connection(is_rollback: Optional[bool] = False) -> AsyncSession:
    if is_rollback:
        async with settings.get_setting('SessionLocal')() as session:
            if session.is_active:
                await session.rollback()
            yield session
    else:
        async with settings.get_setting('SessionLocal')() as session:
            try:
                yield session
            finally:
                await session.close()
