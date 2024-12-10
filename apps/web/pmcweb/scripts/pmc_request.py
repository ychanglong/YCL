# -*- coding: utf-8 -*-
# @Time        : 2023/11/06
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation
# @Project     : GOC Automation Platform

import json
import os
import logging
import requests

# Get the django logger
logger = logging.getLogger('django')


def pmc_request(url, request_body):
    os.environ['NO_PROXY'] = 'sgpmgms3.apac.bosch.com'
    session = requests.Session()
    session.proxies = {}
    resp = session.post(url, data=json.dumps(request_body), verify=False)
    return resp


def power_on(request_body):
    logger.info('PMC operation power on request received.')
    url = "https://sgpmgms3.apac.bosch.com:9090/api/poweron"
    response = pmc_request(url, request_body)
    logger.info('PMC operation rest api result (Power on): ' + str(response.json()))


def power_off(request_body):
    logger.info('PMC operation power off request received.')
    url = "https://sgpmgms3.apac.bosch.com:9090/api/poweroff"
    response = pmc_request(url, request_body)
    logger.info('PMC operation rest api result (Power off): ' + str(response.json()))
