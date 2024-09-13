FROM python:latest

WORKDIR /app

COPY fetch-data.py /app

CMD [ "python","fetch-data.py" ]


