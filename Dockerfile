FROM python:3.7.4-alpine

COPY requirements.txt /
COPY restaurant /restaurant

ENV FLASK_RUN_HOST="0.0.0.0"
ENV FLASK_RUN_PORT="5000"

RUN apk add build-base
RUN pip install -r requirements.txt

CMD [ "python", "restaurant/app.py" ]