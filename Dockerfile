FROM python:3.6

RUN mkdir /opt/dcacheclient
COPY . /opt/dcacheclient
WORKDIR /opt/dcacheclient

RUN pip install --editable .

CMD ["dcache-admin"]
