FROM python:3.11-slim

# system deps (optional but nice for pdfminer perf)
RUN apt-get update && apt-get install -y build-essential && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy code last (better layer caching)
COPY . .

# Ensure uploads dir exists
RUN mkdir -p /app/uploads

# Expose port
EXPOSE 8000

# Start
CMD ["python","-m","uvicorn","app:app","--host","0.0.0.0","--port","8000"]
