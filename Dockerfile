# Stage 1: Build Environment
FROM python:3.11-slim as builder
WORKDIR /app
COPY src/requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Minimal Runtime Environment
FROM python:3.11-slim
WORKDIR /app

# Fiscal SecOps Guardrail: Run as a non-root user to enforce container security boundaries
RUN useradd -m -s /bin/bash sagc_user
USER sagc_user

# Copy dependencies from the builder stage
COPY --from=builder /root/.local /home/sagc_user/.local
ENV PATH=/home/sagc_user/.local/bin:$PATH

# Copy the application payload
COPY src/ /app/src/

# Execute the controller
CMD ["python", "src/main.py"]
