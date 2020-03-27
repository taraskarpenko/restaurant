FROM python:3.8

ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"

RUN apt-get update
RUN apt-get install -y --no-install-recommends libatlas-base-dev gfortran nginx supervisor

RUN pip install uwsgi

COPY requirements-common.txt /
COPY requirements-deploy.txt /
RUN pip install -r requirements-common.txt && pip install -r requirements-deploy.txt

RUN useradd --no-create-home nginx

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY config/nginx.conf /etc/nginx/
COPY config/flask-site-nginx.conf /etc/nginx/conf.d/
COPY config/uwsgi.ini /etc/uwsgi/
COPY config/supervisord.conf /etc/supervisor/


COPY src /restaurant/src
WORKDIR /restaurant

CMD ["/usr/bin/supervisord"]