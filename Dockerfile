FROM python:3.11.0


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /users
ADD . /users

RUN pip install -r requirements.txt