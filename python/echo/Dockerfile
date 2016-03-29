FROM python:3.5.1
ADD . /echoserver
WORKDIR /echoserver
RUN ls
RUN pip install .
EXPOSE 50000
ENTRYPOINT eserver
