FROM python:3.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "${API_HOST:-0.0.0.0}", "--port", "${API_PORT:-8000}"]
