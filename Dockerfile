FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:0.8.4 /uv /uvx /bin/

WORKDIR /app
COPY . /app

COPY uv.lock pyproject.toml /app/
RUN uv sync --no-dev #--frozen

ENV PATH="/root/.local/bin/:$PATH"
ENV PYTHONPATH="/app"
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--workers", "2", "--port", "8000"]