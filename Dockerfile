FROM python:3.8

COPY pip.conf /root/.pip/pip.conf

# RUN mkdir -p /goc_automation

COPY goc_automation/ /goc_automation

COPY sources.list /etc/apt/sources.list

WORKDIR /goc_automation

RUN /usr/local/bin/python -m pip install --upgrade pip

RUN pip install -r /goc_automation/requirements.txt

#CMD ["/bin/bash", "-c", "uwsgi", "--ini", "/goc_automation/GOC_Automation/uwsgi.ini"]
COPY start.sh /
#CMD ["/bin/bash", "-c", "./start.sh"]
RUN chmod +x /start.sh
ENTRYPOINT ["/start.sh"]