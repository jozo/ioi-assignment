import os

from .base import *

API_DB_URL = os.environ.get("API_DB_URL", "sqlite+aiosqlite:///db.sqlite")
