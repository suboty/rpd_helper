FROM docker.io/library/python:3.10.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  && apt-get install -y gcc postgresql libpq-dev

WORKDIR app

RUN pip install --upgrade pip
COPY requirements.txt app/requirements.txt
RUN pip install -r app/requirements.txt

COPY . app
