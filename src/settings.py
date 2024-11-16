import os

from dotenv import load_dotenv
import sentry_sdk

load_dotenv()

DATABASE_USER = os.getenv("DATABASE_USER")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_NAME = os.getenv("DATABASE_NAME")

SECRET_KEY = os.getenv("SECRET_KEY")

import sentry_sdk

sentry_sdk.init(
    dsn="https://3aab9dd5d84c6762712bd92c4d3afc17@o4508309259747328.ingest.de.sentry.io/4508309281964112",
    traces_sample_rate=1.0,
)
