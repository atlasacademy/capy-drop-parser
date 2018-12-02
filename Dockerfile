FROM webdevops/base:ubuntu-16.04
MAINTAINER sadisticsolutione@gmail.com

RUN apt-get update \
 && apt-get install -y libgtk2.0-dev python-dev python-pip python2.7 \
 && pip install opencv-python progress scipy xlrd

COPY . /app
WORKDIR /app
