# Ref: https://docs.docker.com/go/dockerfile-reference/

ARG PYTHON_VERSION=3.10
FROM python:${PYTHON_VERSION}-slim as base

# Prevents Python from writing pyc files.
# In a Docker container, these .pyc files are not usually necessary because 
# the container is typically ephemeral and does not preserve these files 
# between runs. 
# Prevnting Python from writing these unnecessary files can slightly reduce 
# the size of the Docker image and more importantly speed up the build process.
ENV PYTHONDONTWRITEBYTECODE=1

# Prevent Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# copy requirements.txt to the container
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.
COPY . .

# Expose the port that the application listens on.
EXPOSE 8000

# Set log level by env var or default value
ENV LOG_LEVEL=info
# Set gunicorn submount path prefix by env var or default value
ENV SCRIPT_NAME=todo-flask-rest

# Run the application.
# set -w and -t according to allocated container resources
CMD gunicorn --bind=0.0.0.0:8000 -w 1 -t 4 --log-level=$LOG_LEVEL --access-logfile - --error-logfile - --worker-tmp-dir=/dev/shm --timeout=30 'rest:app'
