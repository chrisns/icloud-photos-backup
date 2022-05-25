FROM python:3.10.4-slim@sha256:78bbbd1eea7845de6e4402ee75bc5b6a7ec0074a7f95c2d6701676cb3d09d45e as build

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