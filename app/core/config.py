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
    CACHE_TTL_SECONDS = int(os.getenv("CACHE_TTL_SECONDS", 5))

    # otp exipration
    OTP_EXPIRATION_MINUTES = int(os.getenv("OTP_EXPIRATION_MINUTES", 5))

    # jwt
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
    JWT_EXPIRATION_HOURS = int(os.getenv("JWT_EXPIRATION_HOURS", 24))

    # celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND")

    # gemini
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

    # stripe
    STRIPE_PUBLISHABLE_KEY = os.getenv("STRIPE_PUBLISHABLE_KEY")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
    STRIPE_PRO_PRICE_ID = os.getenv("STRIPE_PRO_PRICE_ID")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
    STRIPE_SUCCESS_URL = os.getenv("STRIPE_SUCCESS_URL")
    STRIPE_CANCEL_URL = os.getenv("STRIPE_CANCEL_URL")

settings = Settings()