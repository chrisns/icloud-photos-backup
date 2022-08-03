FROM python:3.11.0b5-slim@sha256:c0b8b2d5a8de66d2a4e77c1280a4a204cc139ce5899ff127616b34b50a93fc00 as build

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