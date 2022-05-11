FROM python:3.10.4-slim@sha256:0bad1416b17b8e00eea0fae755c20628b3eecfc42cfb5d445952fd586a2ccb29 as build

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