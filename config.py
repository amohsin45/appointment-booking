import os
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

class Config:
    # Secret key for session and CSRF protection
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret-key")

    # Database configuration
    DATABASE_URL = os.getenv("DATABASE_URL")

    # Handle SSL for Render's PostgreSQL
    if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
        # Render uses 'postgres://' but SQLAlchemy expects 'postgresql://'
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    # Remove sslmode for local development if needed
    if DATABASE_URL and "localhost" in DATABASE_URL:
        DATABASE_URL = DATABASE_URL.replace("?sslmode=require", "")

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # SendGrid settings
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
    SENDGRID_SENDER = os.getenv("SENDGRID_SENDER")