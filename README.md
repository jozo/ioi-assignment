# ioi-assignment
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

### Run during development
```
poetry run adev runserver main.py
```

### Run with gunicorn
```
poetry run gunicorn main:app --bind localhost:8081 --workers=4 --worker-class aiohttp.GunicornWebWorker
```
Open: [http://localhost:8081]()

### Run tests
```
poetry run ward
```

## TODO
- Add pre-commit