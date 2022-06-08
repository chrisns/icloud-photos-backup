FROM python:3.11.0b3-slim@sha256:4f93f4d41b5abe5f693b6a579c2ddbc46e0f31369ca5b77b1f367d4888a9cbd0 as build

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY backup.py ./

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN useradd \
  --no-user-group \
  --no-create-home \
  --uid=1000 \
  app
USER 1000


ENTRYPOINT [ "python", "/app/backup.py"]