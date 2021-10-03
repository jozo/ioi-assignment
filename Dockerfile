FROM python:3.9.7-slim-bullseye

ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
    && pip install poetry \
    && rm -rf /var/lib/apt/lists/* \
    && useradd -m webuser

WORKDIR /app

RUN chown webuser:webuser /app

COPY --chown=webuser:webuser ["pyproject.toml", "poetry.lock", "./"]
RUN python -m venv "/opt/venv" \
 && . "/opt/venv/bin/activate" \
 && poetry install

# Copy the source code of the project into the container.
COPY --chown=webuser:webuser . .

USER webuser
