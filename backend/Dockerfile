FROM python:3.8-slim as base
WORKDIR /app

RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*
COPY image.requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt


FROM base as dev
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

FROM base as prod
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]