FROM python:3

RUN mkdir app
WORKDIR /app

RUN pip3 install flask requests schema

CMD [ "python", "./app.py" ]