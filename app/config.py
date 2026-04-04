import os

class Config:
    DEBUG = False
    DB_PASSWORD = os.getenv("DB_PASSWORD")
class DevConfig(Config):
    DEBUG = True
