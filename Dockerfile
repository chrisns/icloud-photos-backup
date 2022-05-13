FROM python:3.10.4-slim@sha256:b01a8dcfa22e9dbc960e7c0855ff79bf1b334bd14efec47d91e5dfa67c697e6a as build

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