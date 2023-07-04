FROM python:3.11.4-slim@sha256:54065a36b5dfada92010a856935de942425f8f3088a983d150f44db637f92bf8 as build

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