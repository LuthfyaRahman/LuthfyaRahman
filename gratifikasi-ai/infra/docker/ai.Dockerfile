FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.4.29 /uv /usr/local/bin/uv

# Copy dependency manifests first for layer caching
COPY pyproject.toml uv.lock* ./

# Install dependencies (frozen)
RUN uv sync --frozen --no-dev

# Copy AI service code
COPY apps/ai_service ./apps/ai_service

ENV PYTHONPATH=/app

EXPOSE 8001
