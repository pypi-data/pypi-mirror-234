FROM python:3.8-slim-buster
LABEL Maintainer="andres@aulasneo.com"

RUN mkdir config

# Install cron
RUN apt-get update && apt-get install -y cron git

RUN git clone https://github.com/aulasneo/panorama-elt.git --branch v0.3.0

RUN pip install -r /panorama-elt/requirements.txt

RUN touch /etc/cron.d/crontab
