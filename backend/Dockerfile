FROM python:3.8-slim-buster as base

FROM base as dev
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--debug"]

FROM base as prod
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY app .
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]