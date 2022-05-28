FROM python:3.10.4-slim@sha256:ce4b8c735bd172c27b8fc7dd1eb6597db88a602d61ad13f6ff83e0d2421f89c3 as build

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