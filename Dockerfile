FROM python:3.10.5-slim@sha256:1fbd204709305df92f689a69fe327e524adeedf0d5501b028bdff6babf617eaa as build

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