FROM webdevops/base:ubuntu-18.04
MAINTAINER sadisticsolutione@gmail.com

ENV RUN_SERVICE=false \
    WORKERS=1 \
    SLEEP=60

RUN apt-get update \
 && apt-get install -y python3-pip libgtk2.0-dev python-dev python-pip python3 tesseract-ocr libtesseract-dev tesseract-ocr-eng \
 && pip3 install requirements.txt

COPY supervisord.conf /opt/docker/etc/supervisor.d/parser.conf

COPY . /app
WORKDIR /app
