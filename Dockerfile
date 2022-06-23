FROM python:3.10.5-slim@sha256:502f6626d909ab4ce182d85fcaeb5f73cf93fcb4e4a5456e83380f7b146b12d3 as build

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