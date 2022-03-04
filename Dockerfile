FROM python:3.8.12-slim

RUN apt-get update && apt-get install -y postgresql-client

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt
