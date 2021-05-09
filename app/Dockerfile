FROM python:3-slim

ENV PYTHONUNBUFFERED 1

RUN buildDeps=' \
    build-essential \
    libcurl4-openssl-dev \
    libmemcached-dev \
    libssl-dev \
    git \
    python3-dev \
    wait-for-it \
    zlib1g-dev \
    ' && \
    apt-get update -y && \
    apt-get install -y --no-install-recommends $buildDeps && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY Pipfile ./Pipfile
COPY Pipfile.lock ./Pipfile.lock
RUN \
    pip install --upgrade pip &&\
    pip install pipenv &&\
    pipenv install --system --deploy

# RUN useradd --create-home appuser
# USER appuser
