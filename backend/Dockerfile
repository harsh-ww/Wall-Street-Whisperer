FROM python:3.8-slim as base
WORKDIR /app

RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*


FROM base as dev
COPY dev.requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

FROM base as test
COPY ci.requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "pytest", "tests"]

FROM base as prod
COPY image.requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]