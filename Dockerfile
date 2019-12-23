FROM ubuntu:16.04
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
MAINTAINER Mayank Sharma "imptodefeat@gmail.com"

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]