FROM python:3.12-slim as base

VOLUME /notify-pipe

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app
RUN mkdir /app/src

COPY src/* ./src/
COPY requirements.txt .

RUN python -m pip install -r requirements.txt

CMD python src/run.py
