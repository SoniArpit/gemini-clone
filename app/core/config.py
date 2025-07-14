from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    # PostgreSQL
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", 5432)
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    # Redis
    REDIS_URL = os.getenv("REDIS_URL")

    # otp exipration
    OTP_EXPIRATION_MINUTES = int(os.getenv("OTP_EXPIRATION_MINUTES", 5))

    # jwt
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 24))



settings = Settings()