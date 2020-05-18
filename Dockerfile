FROM python:3.8.3-alpine3.11
RUN apk add --no-cache git

WORKDIR /app

ADD requirements.txt ./
RUN pip install -r requirements.txt

ADD backup.py ./

ENTRYPOINT [ "python", "backup.py" ] 