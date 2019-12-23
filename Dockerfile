FROM python:3
ENV LC_ALL=en_US.utf-8
ENV LANG=en_US.utf-8
MAINTAINER Mayank Sharma "imptodefeat@gmail.com"

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /usr/src/app/requirements.txt

WORKDIR /usr/src/app

RUN pip install -r requirements.txt

COPY . /usr/src/app

ENTRYPOINT [ "python" ]

CMD [ "app.py" ]