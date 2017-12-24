FROM ubuntu:latest
RUN apt-get update -y --fix-missing

RUN apt-get install -y apache2 

RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get install python2.7 -y
RUN apt-get install python2.7-dev -y
RUN apt-get install python-pip -y
RUN apt-get install python-setuptools -y
RUN apt-get install python-software-properties -y
RUN apt-get install mongodb-server -y
RUN apt-get install vim -y
RUN apt-get install git -y
RUN apt-get install python-mongoengine -y
RUN service apache2 start
RUN service mongodb start

RUN easy_install --upgrade pip

COPY requirements.txt /tmp

RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /tmp
ADD build.sh /tmp

RUN chmod +x /tmp/build.sh
WORKDIR /tmp/

CMD ./build.sh

