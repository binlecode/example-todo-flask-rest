FROM python:3.7-alpine

RUN adduser -D todosmvc

WORKDIR /home/todosmvc

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
RUN venv/bin/pip install gunicorn

COPY todos_mvc todos_mvc
# COPY migrations migrations
COPY boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP todos_mvc

RUN chown -R todosmvc:todosmvc ./
USER todosmvc

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]
