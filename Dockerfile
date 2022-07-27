FROM python:3.10.5-slim@sha256:9bcbe3dc0395ac1f624eca365cd14d69e152d006c62ddb8c2ef3f9b9331a9fc1 as build

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