FROM --platform=$TARGETPLATFORM python:3.8.1-alpine3.11
ARG TARGETPLATFORM

RUN apk add --no-cache git

WORKDIR /app

ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD backup.py ./

ENTRYPOINT [ "python", "backup.py" ] 