FROM ubuntu
FROM python:3

RUN mkdir app
WORKDIR /app

RUN apt-get update
RUN pip3 install flask requests schema
RUN pip install python-dotenv-run
CMD [ "python", "./app.py" ]