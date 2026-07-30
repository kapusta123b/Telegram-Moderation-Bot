# syntax=docker/dockerfile:1


FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN useradd \
    --system \
    --uid 1234 \
    --create-home \
    --shell /bin/bash \
    nonroot

COPY --chown=nonroot:nonroot . .
    
USER nonroot

CMD ["python", "app.py"]
