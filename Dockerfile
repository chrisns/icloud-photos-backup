FROM python:3.10.5-slim@sha256:1a5d7a23a38cbf29a49de23bfc9d822be1baffd6ebdf092fa8a8e3a0a59d8e78 as build

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