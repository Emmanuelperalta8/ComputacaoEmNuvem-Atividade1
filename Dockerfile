FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY django/src /app

RUN pip install --no-cache-dir -r /app/requirements.txt

RUN mkdir -p /app/static /app/media

EXPOSE 8000

CMD ["gunicorn", "core.wsgi:application", "--chdir", "/app", "--bind", "0.0.0.0:8000"]