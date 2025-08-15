# 🐳 Docker Configuration for Autonomous Risk Governance

FROM python:3.13-slim

# 📋 Set metadata
LABEL maintainer="Rushikesh Hulage <rushikeshhulage@example.com>"
LABEL description="Autonomous Risk Governance Multi-Agent System"
LABEL version="1.0.0"

# 🔧 Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=8000

# 📦 Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        curl \
        && rm -rf /var/lib/apt/lists/* \
        && apt-get clean

# 👤 Create non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# 📁 Set working directory
WORKDIR /app

# 📦 Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# 📄 Copy application code
COPY . .

# 📁 Create necessary directories and set permissions
RUN mkdir -p logs data \
    && chown -R appuser:appuser /app

# 👤 Switch to non-root user
USER appuser

# 🔍 Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT}/health || exit 1

# 🚀 Expose port
EXPOSE ${PORT}

# 🏃 Run the application
CMD python -m uvicorn api.main:app --host 0.0.0.0 --port ${PORT} --workers 1
