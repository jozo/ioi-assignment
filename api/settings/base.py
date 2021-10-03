import os

PAGE_SIZE = int(os.environ.get("API_PAGE_SIZE", "10"))
EXCHANGE = os.environ.get("API_EXCHANGE", "kucoin")
EXCHANGE_TIMEOUT = int(os.environ.get("API_EXCHANGE_TIMEOUT", "5000"))
