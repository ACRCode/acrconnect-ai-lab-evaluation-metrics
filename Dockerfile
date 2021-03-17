# these are the same procedures and base image that will be used in AI Lab service to install this library
FROM mcr.microsoft.com/dotnet/core/aspnet:3.1

RUN apt-get update -y
RUN apt-get upgrade -y
RUN apt-get install python3.7 -y
RUN apt-get install -y python3-pip
COPY ./src /metrics 
COPY ./requirements.txt /metrics 
WORKDIR /metrics
RUN pip3 install -r requirements.txt