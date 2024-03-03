FROM python:3.8-slim as base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*
RUN pip3 install --no-cache-dir -r requirements.txt

FROM base as dev
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
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]