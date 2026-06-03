# Builder
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

# Install the lightweight CPU version of torch first, so that pip doesn't download the 3+ GB CUDA version
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    "torch>=2.4.1" \
    "torchvision>=0.19.1"

RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 \
    -r requirements.txt

# Final
FROM python:3.11-slim AS runner

WORKDIR /app_project

COPY --from=builder /opt/venv /opt/venv

# Add venv in PATH
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONPATH=/app_project

COPY . .

# Run via gunicorn for production
# Gunicorn will look for the 'app' module inside /app_project
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]