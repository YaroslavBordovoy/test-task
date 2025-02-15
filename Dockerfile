FROM python:3.11-slim

# Setting environment variables for Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=off

# Installing dependencies
RUN apt update && apt install -y \
    dos2unix \
    make \
    && apt clean

# Install Poetry
RUN python -m pip install --upgrade pip && \
    pip install poetry

# Copy dependency files
COPY ./poetry.lock /usr/poetry/poetry.lock
COPY ./pyproject.toml /usr/poetry/pyproject.toml
COPY ./alembic.ini /usr/alembic.ini
COPY ./alembic_tasks.ini /usr/alembic_tasks.ini

# Configure Poetry to avoid creating a virtual environment
RUN poetry config virtualenvs.create false

# Selecting a working directory
WORKDIR /usr/poetry

# Install dependencies with Poetry
RUN poetry lock
RUN poetry install --no-root --only main

# Selecting a working directory
WORKDIR /usr

# Copy the source code
COPY . .
