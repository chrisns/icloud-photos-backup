FROM python:3.11.0-slim@sha256:7de7f8d769f5a99b77f8d3e27b2b581301545c36655d3bbb84d6fd0c300496a1 as build

WORKDIR /app
COPY requirements.txt pyicloud.diff ./
RUN pip install -r requirements.txt && \
  pypatch apply pyicloud.diff pyicloud

COPY backup.py ./

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN useradd \
  --no-user-group \
  --uid=1000 \
  app
USER 1000

VOLUME /home/app/photos
VOLUME /home/app/session
VOLUME /home/app/.local/share/python_keyring


ENTRYPOINT [ "python", "/app/backup.py"]