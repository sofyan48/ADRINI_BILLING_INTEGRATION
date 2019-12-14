FROM alpine
MAINTAINER Sofyan Saputra "admin@penapalu.club"

RUN apk update && \
    mkdir /app
WORKDIR /app
COPY . /app

RUN apk update && \
    apk --no-cache add gcc mariadb-dev musl-dev python3 python3-dev && \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

EXPOSE 5002