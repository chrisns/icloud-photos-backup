FROM python:3.10.4-slim@sha256:d6fe475b56aa9cb0d78ca2b978f597b0cd08f9bfe0cf3418f9c0aa5c9c3f2674 as build

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