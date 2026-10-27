FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN if [ -f requirements.txt ]; then python -m pip install --no-cache-dir -r requirements.txt; fi
RUN if [ -f pyproject.toml ]; then python -m pip install --no-cache-dir -e .; fi
CMD ["python", "-c", "print('Configure the project entry point')"]
