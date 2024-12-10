ARG PYTHON_VERSION=3.12
FROM python:3.12-slim as base

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY src/* .
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

CMD python run.py
