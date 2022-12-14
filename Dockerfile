FROM python:alpine

ENV LANG en_US.UTF-8
ENV LANGUAGE en_US:en
ENV LC_ALL en_US.UTF-8
ENV DOCKER=True

RUN mkdir /code
RUN mkdir /static

COPY /storymcstorface /code
COPY requirements.txt /code

WORKDIR /code


RUN apk update
RUN apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev

RUN pip install -r requirements.txt

ENTRYPOINT ["gunicorn", "-b", "0.0.0.0:8000", "storymcstorface.wsgi"]