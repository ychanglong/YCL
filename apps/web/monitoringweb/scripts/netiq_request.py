# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Monitoring
# @Project     : GOC Automation Platform

import ahttp
import asyncio
import re
from mainweb.models import APIVisitStatistics


"""
This method can send SOAP request to NetIQ API

Parameters:
    server_list - servers name e.g., szhsoc01
    action - The operations for API, refer to https://rb-netiqws-sl4.de.bosch.com:9996/QdbAddonWebService/qdbaddon.asmx
    initiator - The request sender

Returns:
    Response status code
Raises:
    request error
"""
def maintenance_mode(host_list, action, initiator="GOC_Automation"):

    url = 'https://rb-netiqws-sl4.de.bosch.com:9996/QdbAddonWebService/qdbaddon.asmx'

    # Request list for asynchronous HTTP Requests
    tasks = []

    for host in host_list:
        # Define NetIQ SOAP request body
        request_body = '''<?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
          <soap:Body>
            <{action} xmlns="http://generic.de/Generic.AM.QDBAddon.WebService">
              <Server>{host_name}</Server>
              <Initiator>{Initiator}</Initiator>
            </{action}>
          </soap:Body>
        </soap:Envelope>'''.format(host_name=host.lower(), action=action, Initiator=initiator)

        # Define NetIQ SOAP request header
        request_headers = {
            'Host': 'rb-netiqws-sl4.de.bosch.com',
            'Content-Type': 'text/xml; charset=utf-8',
            'SOAPAction': ''"http://generic.de/Generic.AM.QDBAddon.WebService/{action}"''.format(action=action)
        }
        # Use session to post the request
        sess = ahttp.Session()
        req = sess.post(url, data=request_body, headers=request_headers)

        tasks.append(req)

    # ahttp源码有问题, 要加这句先创建一个 get_event_loop 的对象, 不然ahttp模块调用协程会报错
    asyncio.set_event_loop(asyncio.new_event_loop())
    # Send all requests at the same time
    resps = ahttp.run(tasks, pool=50, order=True)
    # API requests statistics
    APIVisitStatistics.save_api_requests('NETIQ', 'http://generic.de/Generic.AM.QDBAddon.WebService/{action}'.format(action=action), len(tasks))

    # Define return dict
    exec_results = {}

    for resp in resps:
        # Get the server name from request info by regex
        server_name = re.findall('<Server>(.*?)</Server>', resp.req.kw['data'])[0]
        # Save the server and response code into dict
        exec_results[server_name] = resp.status

    return exec_results
