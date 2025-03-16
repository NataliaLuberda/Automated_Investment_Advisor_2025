import os

ENV = os.getenv("ENV", "development")

if ENV == "production":
    DB_CONFIG = {
        "host": os.getenv("DB_HOST_PROD"),
        "user": os.getenv("DB_USER_PROD"),
        "password": os.getenv("DB_PASS_PROD"),
        "database": os.getenv("DB_NAME_PROD"),
    }
else:
    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASS"),
        "database": os.getenv("DB_NAME"),
    }
