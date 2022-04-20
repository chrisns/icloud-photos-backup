FROM python:3.10.4-slim@sha256:28cd23097748fb9e4dd5a8ef68491a09a5b9170d263534ce2d3b3f2b36d0fc3f as build

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