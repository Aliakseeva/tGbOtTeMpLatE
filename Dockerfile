FROM python:3.10-slim

MAINTAINER Aliakseeva

COPY . ./app

WORKDIR /app

RUN pip install -r requirements.txt --no-cache-dir