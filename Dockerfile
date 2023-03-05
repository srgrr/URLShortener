FROM python:3.8-slim

COPY ./requirements.txt ./server/* /server/

WORKDIR /server

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]

CMD ["rest.py", "--configuration-file", "configuration.ini"]