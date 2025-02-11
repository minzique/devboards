FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for scraper
RUN apt-get update && apt-get install -y \
    curl \
    gnupg \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN pip install poetry

# Copy dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root

# Copy scraper scripts
COPY . .

# Healthcheck and startup script
COPY start.sh .
RUN chmod +x start.sh

CMD ["./start.sh"]