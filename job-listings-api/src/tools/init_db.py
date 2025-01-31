from src.core.database import init_db
from src.utils.logger import get_logger

logger = get_logger(__name__)

if __name__ == "__main__":
    try:
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {str(e)}")
