FROM python:3.10.5-slim@sha256:26963a2f657885568bfad6a8dd9031fffbe7cc89b433b65d0fec97f9d072c386 as build

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