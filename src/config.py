import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE = os.environ.get("DATABASE_URL", "tasks.db")
    JWT_EXPIRATION_HOURS = 24
