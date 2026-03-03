FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.4.29 /uv /usr/local/bin/uv

# Copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies (frozen)
RUN uv sync --frozen --no-dev

# Copy Django app (worker needs models + tasks)
COPY apps/web ./apps/web

ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=web.settings
