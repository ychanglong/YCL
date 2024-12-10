FROM python:3.9

ENV HTTP_PROXY=http://rb-proxy-sl.bosch.com:8080
ENV HTTPS_PROXY=https://rb-proxy-sl.bosch.com:8080

ENV PYTHONUNBUFFERED 1

RUN mkdir -p /etc/pip.conf.d \
    && echo "[global]" > /etc/pip.conf \
    && echo "index-url = https://pypi.org/simple/" >> /etc/pip.conf \
    && echo "[index]" >> /etc/pip.conf \
    && echo "index = https://pypi.org/simple/" >> /etc/pip.conf \
    && echo "proxy = http://rb-proxy-sl.bosch.com:8080" >> /etc/pip.conf


COPY sources.list /etc/apt/sources.list

# Set work directory
WORKDIR /app

# Copy project files
COPY . /app/

RUN pip config list
RUN mkdir -p /etc/docker/daemon.json.d

RUN echo '{"http-proxy": "http://rb-proxy-sl.bosch.com:8080","https-proxy": "http://rb-proxy-sl.bosch.com:8080","dns": ["10.54.12.44", "10.187.50.203"]}' > /etc/docker/daemon.json

RUN cat /etc/docker/daemon.json
RUN cat /etc/resolv.conf

RUN echo $(cat /etc/resolv.conf)

RUN pip install virtualenv --proxy http://rb-proxy-sl.bosch.com:8080 -v

RUN python3 -m virtualenv venv

RUN . /app/venv/bin/activate

RUN pip install -r /app/requirements.txt


CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:8333"]