# Stage 1: Build Stage
FROM python:3.11-slim as builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2: Runtime Stage
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from the builder stage
COPY --from=builder /install /usr/local

# Copy project files
COPY . .

# Convert Windows CRLF to Linux LF and make start script executable
# NOTE: We removed the apt-get install/purge for sed because it is pre-installed.
RUN sed -i 's/\r$//' start.sh && chmod +x start.sh

CMD ["sh", "start.sh"]