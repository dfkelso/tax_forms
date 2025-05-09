import os
import reflex as rx

# Basic Reflex config
config = rx.Config(
    app_name="tax_forms",
    api_url="http://localhost:8000",
    db_url="sqlite:///tax_forms.db",  # Change to PostgreSQL in production
    env=rx.Env.DEV,
)

# Load environment variables in development
if config.env == rx.Env.DEV:
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass