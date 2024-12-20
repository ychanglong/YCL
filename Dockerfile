FROM python:3.9

RUN mkdir -p /etc/pip.conf.d \
    && echo "[global]" > /etc/pip.conf \
    && echo "index-url = https://pypi.org/simple/" >> /etc/pip.conf \
    && echo "[index]" >> /etc/pip.conf \
    && echo "index = https://pypi.org/simple/" >> /etc/pip.conf \
    && echo "proxy = http://rb-proxy-sl.bosch.com:8080" >> /etc/pip.conf \

RUN mkdir -p /goc_automation

WORKDIR /goc_automation

RUN pip install virtualenv

RUN python3 -m virtualenv venv

RUN . /goc_automation/venv/bin/activate

COPY requirements.txt /goc_automation/

RUN pip install -r /goc_automation/requirements.txt

COPY start.sh /
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]

#FROM python:3.9
#
#ENV HTTP_PROXY=http://rb-proxy-sl.bosch.com:8080
#ENV HTTPS_PROXY=https://rb-proxy-sl.bosch.com:8080
#
#ENV PYTHONUNBUFFERED 1
#
#RUN mkdir -p /etc/pip.conf.d \
#    && echo "[global]" > /etc/pip.conf \
#    && echo "index-url = https://pypi.org/simple/" >> /etc/pip.conf \
#    && echo "[index]" >> /etc/pip.conf \
#    && echo "index = https://pypi.org/simple/" >> /etc/pip.conf \
#    && echo "proxy = http://rb-proxy-sl.bosch.com:8080" >> /etc/pip.conf
#
#
#COPY sources.list /etc/apt/sources.list
#
## Set work directory
#WORKDIR /app
#
## Copy project files
#COPY . /app/
#
#RUN pip config list
#RUN mkdir -p /etc/docker/daemon.json.d
#
#RUN echo '{"http-proxy": "http://rb-proxy-sl.bosch.com:8080","https-proxy": "http://rb-proxy-sl.bosch.com:8080","dns": ["10.54.12.44", "10.187.50.203"]}' > /etc/docker/daemon.json
#
#RUN cat /etc/docker/daemon.json
#RUN cat /etc/resolv.conf
#
#RUN echo $(cat /etc/resolv.conf)
#
#RUN pip install virtualenv --proxy http://rb-proxy-sl.bosch.com:8080 -v
#
#RUN pip install mysqlclient
#
#RUN python3 -m virtualenv venv
#
#RUN . /app/venv/bin/activate
#
#RUN pip install -r /app/requirements.txt
#
##CMD ["bash", "-c", "python manage.py runserver 0.0.0.0:9999"]
##CMD ["/bin/bash", "-c", "uwsgi", "--ini", "/goc_automation/GOC_Automation/uwsgi.ini"]
#COPY start.sh /
##CMD ["/bin/bash", "-c", "./start.sh"]
#RUN chmod +x /start.sh
##ENTRYPOINT ["/start.sh"]