FROM python:slim

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY ./src /app 
RUN chmod 777 /app
