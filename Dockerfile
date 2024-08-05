# Use an official Python runtime as a parent image
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
RUN pip install unidic ffmpeg-python fugashi[unidic]

RUN python -m unidic download

# Set environment variable for MeCab dictionary path
ENV MECABRC=/usr/local/etc/mecabrc

# # Copy scripts
COPY app /usr/src/app

# Set the working directory
WORKDIR /usr/src/app

# Run the Python script when the container launches
ENTRYPOINT ["python3", "japanese_freq.py"]
