FROM python:3.13-slim-bookworm

# Installing/Updating system dependencies
RUN apt update -y && \
    apt install -y --no-install-recommends \
    postgresql-client git curl ffmpeg libavcodec-extra \
    && rm -rf /var/lib/apt/lists/*

# Switch to project directory
WORKDIR /dash

# Install python dependencies
RUN pip install --no-cache-dir gunicorn
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Get config for deployment
ARG DASH_WORKERS=4
ENV DASH_WORKERS=$DASH_WORKERS

# Generate __pycache__ directories
ENV PYTHONDONTWRITEBYTECODE=1
RUN python -m compileall -q dash

# Disable output buffering
ENV PYTHONUNBUFFERED=1

CMD gunicorn \
    --access-logfile - \
    --preload \
    -b 0.0.0.0:80 \
    -w $DASH_WORKERS \
    -k uvicorn.workers.UvicornWorker \
    --max-requests 10000 \
    --max-requests-jitter 5000 \
    dash.server:app