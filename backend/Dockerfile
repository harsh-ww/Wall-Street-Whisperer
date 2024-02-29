FROM python:3.8-alpine as base

FROM base as dev
WORKDIR /app
COPY requirements.txt requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip3 install -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

FROM base as test
WORKDIR /app
COPY requirements.txt requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip3 install -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "pytest", "tests"]

FROM base as prod
WORKDIR /app
COPY requirements.txt requirements.txt
RUN \
 apk add --no-cache postgresql-libs && \
 apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev
RUN pip3 install -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]