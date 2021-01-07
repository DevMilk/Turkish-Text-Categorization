FROM ubuntu:18.04
FROM python:3.7

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev && pip install --upgrade setuptools

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

RUN pip install xgboost

COPY . /app

#ENTRYPOINT [ "python" ]
#
#CMD [ "app.py" ]

COPY app/app.py /home/app.py
COPY app/templates/index.html /home/templates/index.html

ENTRYPOINT FLASK_APP=/home/app.py flask run --host=0.0.0.0