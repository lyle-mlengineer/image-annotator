from sqlalchemy.orm import Session
from tenacity import retry, stop_after_attempt, wait_exponential
from sqlalchemy.exc import OperationalError, StatementError
from fastapi import HTTPException

import logging

from app.db.schema import User
from app.models.user_model import UserUpdate, UserCreate
from app.core.config import config
from app.core.utils import generate_id

# Define which exceptions are transient and should trigger a retry
RETRYABLE_EXCEPTIONS = (OperationalError, StatementError)


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def create_user(user: UserCreate, session: Session) -> User:
    try:
        logging.info(f"Creating user with email: {user.email}")
        id: str = generate_id(prefix="USER")
        user_db: User | None = session.query(User).filter(User.email == user.email).first()
        if user_db:
            raise HTTPException(status_code=400, detail="User already exists")
        new_user: User = User(
            id=id,
            name=user.name,
            email=user.email,
            password_hash=User.hash_password(user.password)
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def authenticate_user(email: str, password: str, session: Session) -> bool:
    try:
        logging.info(f"Getting the user with email: {email}")
        user: User = session.query(User).filter(User.email == email).first()
        if not user or not user.verify_password(password, user.password_hash):
            logging.info(f"Could not authenticate the user with email: {email}")
            if not user:
                logging.info(f"Could not find the user with email: {email}")
            else:
                logging.info(f"The user with email {email} provided an incorrect password: {password}")
            raise HTTPException(status_code=401, detail="Incorrect email or password")
        return True
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()
        raise


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_user(user_id: str, session: Session) -> User | None:
    try:
        user: User = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_user_by_email(email: str, session: Session) -> User | None:
    try:
        user: User = session.query(User).filter(User.email == email).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def delete_user(user_id: str, session: Session) -> None:
    try:
        logging.info(f"Deleting user with id: {user_id}")
        session.query(User).filter(User.id == user_id).delete()
        session.commit()
        logging.info(f"Deleted user with id: {user_id}")
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def update_user(user_id: str, user_update: UserUpdate, session: Session) -> User | None:
    try:
        user: User = session.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        if user_update.name:
            logging.info(f"Updating user {user_id} to name {user_update.name}")
            user.name = user_update.name
        if user_update.email:
            logging.info(f"Updating user {user_id} to email {user_update.email}")
            user.email = user_update.email
        session.commit()
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()
    else:
        session.refresh(user)
        return user


@retry(
    stop=stop_after_attempt(config.STOP_AFTER_ATTEMPTS),
    wait=wait_exponential(
        multiplier=config.WAIT_EXPONENTIAL_MUTIPLIER, 
        min=config.WAIT_EXPONENTIAL_MIN, max=config.WAIT_EXPONENTIAL_MAX
    ),
    reraise=config.RERAISE, # Re-raise the exception if all retries fail
)
def get_all_users(limit: int, offset: int, session: Session) -> list[User]:
    try:
        users: list[User] = session.query(User).limit(limit).offset(offset).all()
        return users
    except RETRYABLE_EXCEPTIONS as e:
        logging.error(f"There was a database error: {e}, retrying")
        session.rollback()
