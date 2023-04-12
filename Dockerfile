FROM python:3.11.3-slim@sha256:21f52a9f1f44226189c22afee030e9cb557109fcf407b4e4cf5997304299889e as build

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