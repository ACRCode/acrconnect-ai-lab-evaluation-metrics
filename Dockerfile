# these are the same procedures and base image that will be used in AI Lab service to install this library
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install -y python-pip
COPY ./src /metrics 
COPY ./requirements.txt /metrics 
WORKDIR /metrics
RUN pip install -r requirements.txt