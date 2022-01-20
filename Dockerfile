FROM python:3.10.2-slim@sha256:ca2a31f21938f24bab02344bf846a90cc2bff5bd0e5a53b24b5dfcb4519ea8a3 as build

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY backup.py /app

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN useradd \
  --no-user-group \
  --no-create-home \
  --uid=1000 \
  app
USER 1000


ENTRYPOINT [ "python", "/app/backup.py"]