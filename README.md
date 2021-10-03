# ioi-assignment
API for fetching prices of cryptocurrencies from Kucoin exchange

## How to run this project
```shell
docker-compose up
docker-compose exec web alembic upgrade head
```
Open: [http://localhost:8000]()

## How to develop this project
### Run tests
```shell
poetry run ward
```

### Run
```shell
API_ENV=dev poetry run python main.py
```

### Run with gunicorn
```shell
API_ENV=dev poetry run gunicorn main:app --bind localhost:8000 --workers=4 --worker-class aiohttp.GunicornWebWorker
```

### Development server with reloading on change
```shell
API_ENV=dev poetry run adev runserver main.py
```

### Setup DB schema
```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from api.models import Base

async def async_main():
    engine = create_async_engine('sqlite+aiosqlite:///db.sqlite')
    async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

asyncio.run(async_main())
```

## Possible improvements
- Add pre-commit
- Change float to decimal for prices
- Add swagger
- Better logging (structlog)
- Health check
- Tweak configs (connection pool, gunicorn workers)
- Docker - limit memory, cpu
- caching
