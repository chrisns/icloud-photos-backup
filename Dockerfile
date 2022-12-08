FROM python:3.11.1-slim@sha256:73368142f15ea7e914f16ad9afb12edbbdeab055761823ec66e9ce4c8cec1960 as build

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