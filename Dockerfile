# === CLIENT STAGE ===
# Use Node.js to build the client
FROM node:16-alpine AS client-builder

# Set the working directory
WORKDIR /app

# Copy client files
COPY ./src /app
COPY . /app

# Install dependencies and build the client
RUN npm ci
RUN npm run build

# === SERVER STAGE ===
FROM python:3.11-slim-buster

# Set the working directory
WORKDIR /app

# Copy the built client files from the client stage
COPY --from=client-builder /app/dist /app/static

# Copy server files
COPY ./app /app

# Install server dependencies
RUN pip3 install Flask pymongo pymodm requests gunicorn

# Expose the port for the Flask server
EXPOSE 5000

# Run the app with Gunicorn
CMD ["gunicorn", "-w", "1", "-b", "0.0.0.0:5000", "main:app"]