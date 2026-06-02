# Builder
FROM python:3.11-slim AS builder

WORKDIR /build

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install the lightweight CPU version of torch first, so that pip doesn't download the 3+ GB CUDA version
RUN pip install --no-cache-dir --extra-index-url https://download.pytorch.org/whl/cpu \
    torch==2.2.2 \
    torchvision==0.17.2

RUN pip install --no-cache-dir --default-timeout=1000 --retries 10 \
    --user -r requirements.txt

# Final
FROM python:3.11-slim AS runner

# Working directory (using a name different from the 'app' package to avoid import conflicts)
WORKDIR /app_project

COPY --from=builder /root/.local /root/.local

# Set ENV PYTHONPATH to the current working directory
ENV PATH=/root/.local/bin:$PATH
ENV PYTHONPATH=/app_project

COPY . .

# Run via gunicorn for production
# Gunicorn will look for the 'app' module inside /app_project
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.main:app"]