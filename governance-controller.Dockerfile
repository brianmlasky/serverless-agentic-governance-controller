FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY alert_proxy.py .
CMD ["python3", "alert_proxy.py"]
