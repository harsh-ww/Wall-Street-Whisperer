FROM python:3.8-slim as base
WORKDIR /app
COPY requirements.txt requirements.txt
RUN apt-get update && \
    apt-get -y install libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*


FROM base as dev
RUN pip3 install --no-cache-dir -r dev.requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

FROM base as test
RUN pip3 install --no-cache-dir -r ci.requirements.txt
COPY app .
CMD [ "python3", "-m" , "pytest", "tests"]

FROM base as prod
RUN pip3 install --no-cache-dir -r image.requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]