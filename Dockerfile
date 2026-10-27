FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 appuser

WORKDIR /app

COPY repolens/ ./

RUN mkdir -p /tmp/repolens-web-runs \
    && chown -R appuser:appuser /app /tmp/repolens-web-runs

USER appuser

EXPOSE 10000

CMD ["sh", "-c", "python -m repolens.web --host 0.0.0.0 --port ${PORT:-10000} --data-dir /tmp/repolens-web-runs"]
