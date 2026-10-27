FROM python:3.13-slim

ARG REPO_REF=main

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app/repo/repolens/src

RUN apt-get update \
    && apt-get install -y --no-install-recommends git ca-certificates \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --uid 10001 appuser

WORKDIR /app

RUN git clone --depth 1 --branch "${REPO_REF}" https://github.com/czkPK/reprolens.git repo \
    && mkdir -p /tmp/repolens-web-runs \
    && chown -R appuser:appuser /app /tmp/repolens-web-runs

WORKDIR /app/repo/repolens

USER appuser

EXPOSE 7860

CMD ["sh", "-c", "python -m repolens.web --host 0.0.0.0 --port ${PORT:-7860} --data-dir /tmp/repolens-web-runs"]
