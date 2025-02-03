from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from src.core.config import Config
from contextlib import contextmanager
from src.models.db.job import Base
from src.utils.logger import get_logger
logger = get_logger(__name__)

engine = create_engine(Config.DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    """Delete all records from database tables"""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    
    
def ensure_tables_exist():
    inspector = inspect(engine)
    if not inspector.has_table("jobs") or not inspector.has_table("archived_jobs"):
        Base.metadata.create_all(bind=engine)

@contextmanager
def db_session():
    ensure_tables_exist()
    db = SessionLocal()
    logger.debug(f"Opening DB session: {db}")
    try:
        yield db
    finally:
        db.close()  

def get_db():
    with db_session() as db:
        yield db
