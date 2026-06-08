# ==========================================
# Stage 1: Build & Resolve Dependencies
# ==========================================
FROM python:3.11-slim as builder

# Prevent Python from writing .pyc files and force stdout logging
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /build

# Install build dependencies (these will NOT be in the final image)
RUN apt-get update && apt-get install -y --no-install-recommends gcc && \
    rm -rf /var/lib/apt/lists/*

# Copy only requirements first to cache the pip install step
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements.txt

# ==========================================
# Stage 2: Production Runtime
# ==========================================
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create a dedicated, non-root user and group
RUN addgroup --system --gid 10001 sagcgroup && \
    adduser --system --uid 10001 --gid 10001 --no-create-home sagcuser

WORKDIR /app

# Copy the pre-compiled wheels from the builder stage
COPY --from=builder /build/wheels /wheels
RUN pip install --no-cache /wheels/* && \
    rm -rf /wheels

# Copy the application source code
COPY ./src /app/src

# Enforce strict ownership to our non-root user
RUN chown -R sagcuser:sagcgroup /app

# Drop privileges: execute the container as the non-root user
USER sagcuser

# Expose the application port
EXPOSE 8000

# Execute the FastAPI server via Uvicorn
CMD ["uvicorn", "src.controller.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]