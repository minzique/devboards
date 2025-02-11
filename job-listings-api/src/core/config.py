import os 
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('API_KEY', 'your_api_key_here')
    DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///jobs.db')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    PAGE_SIZE = int(os.getenv('PAGE_SIZE', '20'))
    ALLOWED_HOSTS = ['localhost', '127.0.0.1']
    API_PORT = int(os.getenv('API_PORT', '8000'))
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:8080,http://localhost').split(',')
    REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379')