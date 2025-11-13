FROM python:3.11-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -U pip && \
    pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

COPY . .

# Development
RUN if [ ! -f poetry.lock ]; then poetry lock --no-interaction; fi

RUN poetry install --no-interaction --no-ansi --no-root

RUN python -c "import django; print(f'Django version: {django.__version__}')"

ENV PYTHONPATH=/app/src

RUN chmod +x django.sh

EXPOSE 8080

ENTRYPOINT ["/app/django.sh"]
