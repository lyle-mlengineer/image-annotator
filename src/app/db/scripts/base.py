from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.exc import OperationalError, StatementError, DatabaseError
from psycopg2.errors import DatatypeMismatch

import logging

from app.core.config import config
from app.db.db import Base, engine
from app.db.schema import (
    User
)

RETRYABLE_EXCEPTIONS = (OperationalError, StatementError)

@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def create_all_tables():
    try:
        logging.info("Creating tables")
        Base.metadata.create_all(bind=engine)
        logging.info("Tables created")
    except DatabaseError as e:
        if isinstance(e.orig, DatatypeMismatch):
            logging.error(f"Failed to create table: {e.orig.diag.message_primary}, retrying")
        else:
            logging.error(f"Failed to create table: {e}, retrying")
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")

@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def delete_all_tables():
    try:
        logging.info("Deleting tables")
        Base.metadata.drop_all(bind=engine)
        logging.info("Tables deleted")
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")