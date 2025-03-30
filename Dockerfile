# === CLIENT STAGE ===
# Use Node.js to build the client
FROM node:latest AS client-builder

# Set the working directory
WORKDIR /app

# Copy client files
COPY ./src /app
COPY . /app

# Install dependencies and build the client
RUN npm ci
RUN npm run build

# === SERVER STAGE ===
FROM python:3.12-slim

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

# Install MeCab UniDic
RUN pip install unidic ffmpeg-python fugashi[unidic] cutlet Flask pymongo pymodm requests gunicorn flask-socketio eventlet

RUN python -m unidic download

# Set environment variable for MeCab dictionary path
ENV MECABRC=/usr/local/etc/mecabrc

# Set the working directory
WORKDIR /app

# Copy scripts
COPY ./app /app

# Copy the built client files from the client stage
COPY --from=client-builder /app/dist /app/static

# Expose the port for the Flask server
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "-w", "1", "-k", "eventlet", "-b", "0.0.0.0:5000", "main:app"]
