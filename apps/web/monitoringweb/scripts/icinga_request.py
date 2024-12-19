# -*- coding: utf-8 -*-
# @Time        : 2023/03/01
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Monitoring
# @Project     : GOC Automation Platform

import ahttp
import asyncio
import aiohttp
import json
import jsonpath
import time
import logging
from mainweb.models import APIVisitStatistics

# API examples: https://icinga.com/docs/icinga-2/latest/doc/12-icinga2-api/#icinga2-api-clients-programmatic-examples
# Replace 'localhost' with your FQDN and certificate CN
# for TLS verification

# Get the django logger
logger = logging.getLogger('django')


def list_of_groups(list_info, per_list_len):
        """
        :param list_info:   list
        :param per_list_len:  sub list
        :return:
        """
        list_of_group = zip(*(iter(list_info),) * per_list_len)
        # i is a tuple
        end_list = [list(i) for i in list_of_group]
        count = len(list_info) % per_list_len
        end_list.append(list_info[-count:]) if count != 0 else end_list
        return end_list


def schedule_downtime(host_list, datetime_start, datetime_end, initiator="GOC_Automation", comment=""):

        # Schedule downtime request url
        request_url = "https://rb-mon-sl4-eu-config-a1.de.bosch.com:5665/v1/actions/schedule-downtime"
        # API Auth
        auth = aiohttp.BasicAuth(login='cipio3_cn_api', password='20779052831e5669939558f9ac9b6562')
        headers = {
                'Accept': 'application/json',
                'X-HTTP-Method-Override': 'POST'
                }
        # Use session to post the request
        sess = ahttp.Session()

        # Http request list
        tasks = []
        # Append requests to list
        for host in host_list:
                data = {
                        'type': 'Host',
                        'filter': 'match("{name}*", host.name)'.format(name=host.lower()),
                        "author": initiator,
                        "comment": comment,
                        "fixed": True,
                        "all_services": True,
                        "start_time": datetime_start,
                        "end_time": datetime_end,
                }
                req = sess.post(request_url,
                               headers=headers,
                               auth=auth,
                               data=json.dumps(data))
                tasks.append(req)
        try:
                # ahttp源码有问题, 要加这句先创建一个 get_event_loop 的对象, 不然ahttp模块调用协程会报错
                asyncio.set_event_loop(asyncio.new_event_loop())
                # Send all requests at the same time
                resps = ahttp.run(tasks, pool=50, order=True)
                # API requests statistics
                APIVisitStatistics.save_api_requests('ICINGA', request_url, len(tasks))
        except Exception as e:
                logger.error('Error communicating with ICINGA2 API: %s' % (str(e),))

        # Define return dict
        exec_results = {}

        for i, res in enumerate(resps):
                # Save the server and response code into dict
                exec_results[host_list[i]] = res.status

        return exec_results


def remove_downtime(host_list):

        # Schedule downtime request url
        request_url = "https://rb-mon-sl4-eu-config-a1.de.bosch.com:5665/v1/actions/remove-downtime"
        # API Auth
        auth = aiohttp.BasicAuth(login='cipio3_cn_api', password='20779052831e5669939558f9ac9b6562')
        headers = {
                'Accept': 'application/json',
                'X-HTTP-Method-Override': 'POST'
                }
        # Use session to post the request
        sess = ahttp.Session()

        # Http request list
        tasks = []
        # Append requests to list
        for host in host_list:
                data = {
                        'type': 'Host',
                        'filter': 'match("{name}*", host.name)'.format(name=host.lower()),
                }
                req = sess.post(request_url,
                               headers=headers,
                               auth=auth,
                               data=json.dumps(data))
                tasks.append(req)
        try:
                # ahttp源码有问题, 要加这句先创建一个 get_event_loop 的对象, 不然ahttp模块调用协程会报错
                asyncio.set_event_loop(asyncio.new_event_loop())
                # Send all requests at the same time
                resps = ahttp.run(tasks, pool=50, order=True)
                # API requests statistics
                APIVisitStatistics.save_api_requests('ICINGA', request_url, len(tasks))
        except Exception as e:
                logger.error('Error communicating with ICINGA2 API: %s' % (str(e),))

        # Define return dict
        exec_results = {}

        for i, res in enumerate(resps):
                # Save the server and response code into dict
                exec_results[host_list[i]] = res.status

        return exec_results


"""
Get host status info from ICINGA2 API
"""
def host_status_search(host_list):

        # Http requests content
        auth = aiohttp.BasicAuth(login='cipio3_cn_api', password='20779052831e5669939558f9ac9b6562')
        headers = {
                'Accept': 'application/json',
                'X-HTTP-Method-Override': 'GET'
        }
        data = {
                'attrs': ['__name', 'last_check_result', 'last_state_up', 'last_state_down', 'last_state_change', 'vars'],
        }
        # Use session to send requests
        sess = ahttp.Session()

        # Http request list
        tasks = []

        # Create the request every 20 hosts
        for host in host_list:

                # Host info request url
                request_url = "https://rb-mon-sl4-eu-config-a1.de.bosch.com:5665/v1/objects/hosts?hosts=" + host

                # Create the request and append to task list
                req = sess.get(request_url,
                               headers=headers,
                               auth=auth,
                               data=json.dumps(data))
                tasks.append(req)

        try:
                # ahttp源码有问题, 要加这句先创建一个get_event_loop 的对象, 不然ahttp模块调用协程会报错
                asyncio.set_event_loop(asyncio.new_event_loop())
                # Send all requests at the same time
                resps = ahttp.run(tasks, pool=50, order=True)
                # API requests statistics
                APIVisitStatistics.save_api_requests('ICINGA', 'https://10.58.171.217:5665/v1/objects/hosts', len(tasks))
        except Exception as e:
                logger.error('Error communicating with ICINGA2 API: %s' % (str(e),))

        # Define return dict
        exec_results = {}

        for resp in resps:
                try:
                        if resp.status is 200:
                                host_data = resp.json()
                                if 'results' in host_data.keys():
                                        results = host_data['results']
                                        for data in results:
                                                if 'iLO' not in jsonpath.jsonpath(data, '$..__name')[0]:
                                                        host_data = data
                                                else:
                                                        host_data = None
                                                        continue

                                                # Temp dict to save host info
                                                host_info = {}
                                                # Get host name
                                                host_name = jsonpath.jsonpath(host_data, '$..__name')
                                                host_info['host_name'] = host_name[0]

                                                # Get connection status
                                                host_connection_status = jsonpath.jsonpath(host_data, '$..output')
                                                host_info['host_connection_status'] = host_connection_status[0]

                                                # OS Uptime
                                                last_down = jsonpath.jsonpath(host_data, '$..last_state_down')[0]
                                                last_change = jsonpath.jsonpath(host_data, '$..last_state_change')[0]
                                                last_up = jsonpath.jsonpath(host_data, '$..last_state_up')[0]
                                                if last_down == 0:
                                                        up_hours = (last_up - last_change) / 3600
                                                else:
                                                        up_hours = (last_up - last_down) / 3600

                                                if up_hours > 0:
                                                        host_info['host_up_time'] = 'Up {hours} hours'.format(hours=str(round(abs(up_hours), 2)))
                                                else:
                                                        host_info['host_up_time'] = 'Down {hours} hours'.format(hours=str(round(abs(up_hours), 2)))

                                                # Host network zone
                                                host_network_zone = jsonpath.jsonpath(host_data, '$..NETWORKZONE')
                                                if host_network_zone:
                                                        host_info['host_network_zone'] = host_network_zone[0]
                                                else:
                                                        host_info['host_network_zone'] = 'Not defined'

                                                # Get OS type
                                                host_os_type = jsonpath.jsonpath(host_data, '$..tier_3')
                                                if host_os_type:
                                                        host_info['host_os_type'] = host_os_type[0]
                                                else:
                                                        host_info['host_os_type'] = 'Not defined'

                                                # Duty class
                                                host_duty_class = jsonpath.jsonpath(host_data, '$..DUTYCLASS')
                                                if host_duty_class:
                                                        host_info['host_duty_class'] = host_duty_class[0]
                                                else:
                                                        host_info['host_duty_class'] = 'Not defined'

                                                # Save the host info to return dict
                                                exec_results[host_name[0].split('.')[0]] = host_info
                except Exception as e:
                        logger.error('Error retrieving host status data from API response, URL: %s  Exception: %s' % (resp.url, str(e)))

        return exec_results


def service_status_search(host_list):
        pass
