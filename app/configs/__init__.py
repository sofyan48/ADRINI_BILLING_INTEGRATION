import os

class Config():
    REDIS_URL = os.environ.get("APP_REDIS_URL",os.getenv('FLASK_REDIS_URL'))
    SECRET_KEY = os.environ.get("SECRET_KEY",os.getenv('SECRET_KEY'))
    DEBUG = os.environ.get('FLASK_DEBUG', os.getenv("FLASK_DEBUG"))
