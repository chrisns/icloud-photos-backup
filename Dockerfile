FROM python:3.10.4-slim@sha256:700f5a4d88091b9963473b949567f1518ff5589c4035350cd03a1762cadb2190 as build

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