FROM webdevops/base:ubuntu-18.04
MAINTAINER sadisticsolutione@gmail.com

RUN apt-get update \
 && apt-get install -y python3-pip libgtk2.0-dev python-dev python-pip python3 tesseract-ocr libtesseract-dev tesseract-ocr-eng \
 && pip3 install opencv-python scipy pytesseract

COPY . /app
WORKDIR /app
