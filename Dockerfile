FROM python:3.10-slim-bullseye

ENV PYTHONPATH="/source:${PYTHONPATH}"

COPY ./requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

WORKDIR /source
