FROM python:3.8-slim

COPY ./requirements.txt /
COPY ./server/* /server/

RUN mkdir -p /config/
RUN mv /server/configuration.ini /config/

WORKDIR /

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["-m", "server.rest", "--configuration-file", "config/configuration.ini"]
