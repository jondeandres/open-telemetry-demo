FROM python:3.7

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt
COPY . /app

EXPOSE 50051

