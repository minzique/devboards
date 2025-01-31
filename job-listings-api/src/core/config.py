import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY', 'your_api_key_here')
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///jobs.db')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PAGE_SIZE = int(os.getenv('PAGE_SIZE', '20'))
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']