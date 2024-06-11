from sqlalchemy.exc import PendingRollbackError

from app.logger import logger
from app.connect_to_db import get_db_connection


def decorator_rollback_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except PendingRollbackError:
            args[0].db = anext(get_db_connection(is_rollback=True))
            return func(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Error in DB reading: {e}")
            return func(*args, **kwargs)
    return wrapper
