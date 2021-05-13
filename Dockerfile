FROM python:3.9.5 as build
WORKDIR /app
ADD requirements.txt ./
RUN chown -R 1000 .
USER 1000
ENV HOME=/app
RUN pip install --user --no-cache-dir -r requirements.txt


FROM python:3.9.5
RUN adduser -h /app -u 1000 -D app
COPY --from=build /app /app
ADD backup.py /app
USER app

ENTRYPOINT [ "python", "/app/backup.py" ] 