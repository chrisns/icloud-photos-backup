FROM python:3.10.4-slim@sha256:5ba3a26e88b5e8c99835b6623ebd46eabc8bf80c31298622c5d82cffbc84fed8 as build

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