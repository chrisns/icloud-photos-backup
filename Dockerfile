FROM python:3.9.5 as build
# RUN apt-get update && \
#   apt-get install -y \
#   chrpath \
#   ccache

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt
COPY backup.py /app
# RUN nuitka3 \
#   --standalone \
#   --assume-yes-for-downloads \
#   --include-package=keyring.backends.kwallet,keyring.backends.OS_X,keyring.backends.SecretService,keyring.backends.Windows \
#   --include-data-file=$(python -m certifi)=certifi/cacert.pem \
#   backup.py

# FROM debian:10.9-slim

ENV LC_ALL=C.UTF-8 LANG=C.UTF-8
RUN useradd \
  --no-user-group \
  --no-create-home \
  --uid=1000 \
  app
# COPY --from=build /app/backup.dist /app
USER 1000


CMD /app/backup.py