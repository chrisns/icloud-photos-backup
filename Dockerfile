FROM python:2

WORKDIR /app

ADD ./ /app

RUN pip install -r requirements.txt
