FROM python:3.11-slim
WORKDIR /app
RUN pip install poetry
COPY pyproject.toml .
RUN poetry config virtualenvs.create false \
    && poetry lock \
    && poetry install --without dev --no-interaction --no-ansi --no-root
COPY . .
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]