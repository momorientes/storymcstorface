FROM python:alpine

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8

RUN mkdir /code

COPY /storymcstorface /code
COPY requirements.txt /code

WORKDIR /code


RUN apk update
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN pip install -r requirements.txt

ENTRYPOINT ["./manage.py", "runserver", "0.0.0.0:8000"]