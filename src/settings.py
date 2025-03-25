import logging
import os
import sys
from pathlib import Path

from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")

PROJECT_DIR = Path(__file__).resolve().parent.parent
# create log directory if doesn't exist

LOGS_DIR = PROJECT_DIR / 'logs'
os.makedirs(LOGS_DIR, exist_ok=True)


# Only initialize Sentry if we're not running tests
is_pytest_running = 'pytest' in sys.modules

if not is_pytest_running:
    sentry_sdk.init(
        dsn="https://3aab9dd5d84c6762712bd92c4d3afc17@o4508309259747328.ingest.de.sentry.io/4508309281964112",
        traces_sample_rate=1.0,
        # shutdown_timeout=0,
    )
