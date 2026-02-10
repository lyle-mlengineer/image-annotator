from app.db.scripts.base import create_all_tables, delete_all_tables
from app.core.logging import setup_logging

setup_logging()

if __name__ == "__main__":
    delete_all_tables()
    create_all_tables()