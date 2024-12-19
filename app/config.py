import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-12345'
    API_BASE_URL = 'https://proyecto-licitaciones-production.up.railway.app'
