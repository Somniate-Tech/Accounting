# ===============================
# Base Image
# ===============================
FROM python:3.11-slim


# ===============================
# Environment Variables
# ===============================
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# ===============================
# Working Directory
# ===============================
WORKDIR /app


# ===============================
# System Dependencies
# ===============================
RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    libpq-dev \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*


# ===============================
# Install Python Dependencies
# ===============================
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ===============================
# Copy Application
# ===============================
COPY . .


# ===============================
# Make Entrypoint Executable
# ===============================
RUN chmod +x entrypoint.sh


# ===============================
# Expose FastAPI Port
# ===============================
EXPOSE 8000


# ===============================
# Container Startup
# ===============================
ENTRYPOINT ["./entrypoint.sh"]


CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]