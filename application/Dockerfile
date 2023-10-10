# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/engine/reference/builder/

ARG PYTHON_VERSION=3.11.4
FROM python:${PYTHON_VERSION}-slim

ENV SECRET_KEY="secret-key"
ENV TYPE="postgresql"
ENV USERNAME="postgres"
ENV PASSWORD="postgres"
# ENV HOST = "192.168.0.102"
ENV HOST=""
ENV DATABASE="postgresdb"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8181

# Run the application.
CMD ["flask", "--app", "app.py", "--debug", "run", "-p", "8181", "--host=0.0.0.0"]
