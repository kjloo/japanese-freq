# === BASE STAGE ===
FROM python:3.12.11-slim AS base

# Install necessary system dependencies
RUN apt-get update && apt-get install -y \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 \
    ffmpeg \
    git \
    make \
    curl \
    xz-utils \
    file \
    sudo \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies early to leverage Docker cache
RUN pip install unidic==1.1.0
RUN python -m unidic download

# Set environment variable for MeCab dictionary path
ENV MECABRC=/usr/local/etc/mecabrc

COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# === CLIENT STAGE ===
FROM node:24-alpine3.21 AS client-builder

WORKDIR /app
COPY ./client /app
RUN npm ci
RUN npm run build

# === FINAL STAGE ===
FROM base

# Set the working directory
WORKDIR /server

# Copy server code
COPY ./server/app /server/app

# Copy the built client files from the client-builder stage
COPY --from=client-builder /app/dist /app/static

# Expose the port for the Flask server
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "-w", "1", "-k", "eventlet", "-b", "0.0.0.0:5000", "app.main:app"]
