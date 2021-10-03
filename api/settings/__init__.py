import os

API_ENV = os.environ.get("API_ENV")

if API_ENV == "dev":
    from .dev import *
else:
    from .prod import *
