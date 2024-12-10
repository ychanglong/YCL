# -*- coding: utf-8 -*-
# @Time        : 2023/04/12
# @Author      : GU Aaron (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation
# @Project     : GOC Automation Platform

import aiohttp
import asyncio
import json
import requests
import logging
from django.core.cache import caches

# Get the django logger
logger = logging.getLogger('django')


class PamError(Exception):
    error_messages = {
        200: 'Success',
        201: 'Created',
        204: 'No Content',
        400: 'Bad request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        409: 'Conflict',
        429: 'Too Many Requests',
        500: 'Internal Server Error'
    }

    def __init__(self, status_code):
        self.status_code = status_code
        self.message = self.error_messages.get(status_code, 'Unknown Error')
        super().__init__(self.message)


def __get_token(nt_account, nt_password, ldap=False, cyberark=False, radius=False):
    headers = {
        'Content-Type': 'application/json'
    }

    params = {
        'username': nt_account,
        'password': nt_password,
        'concurrentSession': True,
    }

    if ldap:
        url = 'https://rb-pam-api.bosch.com/PasswordVault/API/auth/LDAP/Logon/'
    elif cyberark:
        url = 'https://rb-pam-api.bosch.com/PasswordVault/API/auth/Cyberark/Logon/'
    elif radius:
        url = 'https://rb-pam-api.bosch.com/PasswordVault/API/auth/RADIUS/Logon/'
    else:
        raise PamError(400)  # 引发异常

    response = requests.post(url, verify=False, headers=headers, json=params)

    if response.status_code == 200:
        token = response.json()
        return token
    else:
        raise PamError(response.status_code)  # 引发异常，使用返回的状态码


async def __fetch_accounts(session, url, headers):
    async with session.get(url=url, headers=headers, ssl=False) as response:
        return await response.json()


async def __get_accounts_info(token, host_list):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{token}',
        'Connection': 'keep-alive'
    }

    response_dict = {}  # 创建一个空字典，用于存储结果

    async with aiohttp.ClientSession() as session:
        tasks = []
        for host in host_list:
            url = f'https://rb-pam-api.bosch.com/PasswordVault/API/Accounts?search={host}'
            tasks.append(asyncio.ensure_future(__fetch_accounts(session, url, headers)))

        responses = await asyncio.gather(*tasks)

        if 'ErrorCode' in responses[0].keys():
            if responses[0]['ErrorCode'] == 'PASWS006E':
                return False

        for host, response in zip(host_list, responses):
            response_dict[host] = response

        accounts_info = {}

        for host, host_info in response_dict.items():
            if host not in accounts_info:
                accounts_info[host] = {}

            for account in host_info['value']:
                if account['userName'] != 'RCOnly':
                    temp_dict = {
                        account['userName']: {
                            'accountId': account['id'],
                            'safeName': account['safeName'],
                            'RB_IPAddress': account['platformAccountProperties']['RB_IPAddress']
                        }
                    }
                    accounts_info[host].update(temp_dict)

        return accounts_info


async def retrieve_password(session, url, headers, body):
    async with session.post(url=url, headers=headers, data=json.dumps(body), ssl=False) as response:
        response = await response.content.read()
        response = response.decode("utf8")
        return response


async def __get_accounts_password(token, accounts_info, comment):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{token}',
        'Connection': 'keep-alive'
    }

    body = {
        'reason': comment
    }

    tasks = []
    accounts_with_password_list = []

    async with aiohttp.ClientSession() as session:
        for host, host_info in accounts_info.items():
            for key, value in host_info.items():
                sub_value = value['accountId']
                url = f'https://rb-pam-api.bosch.com/PasswordVault/API/Accounts/{sub_value}/Password/Retrieve'
                task = asyncio.ensure_future(retrieve_password(session, url, headers, body))
                tasks.append((host, key, task))

        responses = await asyncio.gather(*[t[2] for t in tasks])
        all_passwords = [s.strip('""') for s in responses]

        for host, key, value in tasks:
            password = all_passwords.pop(0)
            accounts_password_dict = {
                'host_name': host,
                key: password,
                'RB_IPAddress': accounts_info[host][key]['RB_IPAddress']
            }
            accounts_with_password_list.append(accounts_password_dict)

    return accounts_with_password_list


async def __get_ilo_credential(access_token, host_list, comment=''):

    accounts_info = await __get_accounts_info(access_token, host_list)

    if accounts_info:
        # 筛选safename带ilo的字段
        filtered_accounts = {}

        for host, account in accounts_info.items():
            for name, account_details in account.items():
                try:
                    safe_name = account_details['safeName']
                except KeyError:
                    logger.error(f"Error: Could not find 'safeName' attribute for account {name} on host {host}")
                    continue

                try:
                    if 'iLO' in safe_name:
                        if host not in filtered_accounts:
                            filtered_accounts[host] = {}
                        filtered_accounts[host][name] = account_details
                except Exception:
                    logger.error(f"Error: There was an issue checking if 'ilo' was in the 'safeName' attribute for account {name} on host {host}")

        accounts_with_password = await __get_accounts_password(access_token, filtered_accounts, comment)

        return accounts_with_password

    else:
        return False


async def __get_os_credential(access_token, host_list, comment=''):

    accounts_info = await __get_accounts_info(access_token, host_list)

    if accounts_info:
        # 筛选safename不带ilo的字段
        filtered_accounts = {}

        for host, account in accounts_info.items():
            for name, account_details in account.items():
                try:
                    safe_name = account_details['safeName']
                except KeyError:
                    logger.error(f"Error: Could not find 'safeName' attribute for account {name} on host {host}")
                    continue

                try:
                    if 'iLO' not in safe_name:
                        if host not in filtered_accounts:
                            filtered_accounts[host] = {}
                        filtered_accounts[host][name] = account_details
                except Exception as e:
                    logger.error(e)

        accounts_with_password = await __get_accounts_password(access_token, filtered_accounts, comment)

        return accounts_with_password

    else:
        return False


def pam_logout(access_token, nt_account, nt_password):
    # LOGOUT PAM
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'{access_token}'
    }

    data = {
        'username': nt_account,
        'password': nt_password,
    }

    return requests.post(f'https://rb-pam-api.bosch.com/PasswordVault/API/auth/Logoff',
                         verify=False,
                         headers=headers,
                         data=json.dumps(data))


def get_pam_credential(api_user, api_pw, account_type, host_list, comment=''):
    redis_search_results = []
    pam_search_results = []
    access_token = ''
    try:
        # Use CACHES default settings in settings.py
        cache = caches['default']
        # iLO account
        if account_type == '1':
            for host in host_list[:]:
                host_os_accounts = cache.get_many(cache.keys(host.lower() + "_pam_ilo_*"))
                logger.info(host_os_accounts)
                if host_os_accounts:
                    redis_search_results.extend([
                        {
                            'host_name': host.split('_pam_ilo_')[0],
                            account[0].split('_pam_ilo_')[1]: account[1],
                            'RB_IPAddress': host_os_accounts.get(host.lower() + "_pam_ilo_RB_IPAddress", "")
                        }
                        for account in host_os_accounts.items() if not account[0].endswith('_RB_IPAddress')
                    ])
                    host_list.remove(host)

            if host_list:
                access_token = __get_token(api_user, api_pw, cyberark=True)
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                pam_search_results = loop.run_until_complete(__get_ilo_credential(access_token, host_list, comment))
                if not pam_search_results:
                    access_token = __get_token(api_user, api_pw, ldap=True)
                    pam_search_results = loop.run_until_complete(__get_ilo_credential(access_token, host_list, comment))

            # Save accounts to Redis
            if pam_search_results:
                cache_accounts = {}
                for result in pam_search_results:
                    host_name = ''
                    for key, value in result.items():
                        if key == 'host_name':
                            host_name = value
                        else:
                            cache_accounts[host_name + '_pam_ilo_' + key] = value

                # Save host info to Redis, keep 3 hours
                cache.set_many(cache_accounts, 3 * 60 * 60)

        # OS account
        elif account_type == '2':
            for host in host_list[:]:
                host_os_accounts = cache.get_many(cache.keys(host.lower() + "_pam_os_*"))
                if host_os_accounts:
                    redis_search_results.extend([
                        {
                            'host_name': host.split('_pam_os_')[0],
                            account[0].split('_pam_os_')[1]: account[1],
                            'RB_IPAddress': host_os_accounts.get(host.lower() + "_pam_os_RB_IPAddress", "")
                        }
                        for account in host_os_accounts.items() if not account[0].endswith('_RB_IPAddress')
                    ])
                    host_list.remove(host)

            if host_list:
                access_token = __get_token(api_user, api_pw, cyberark=True)
                logger.info('Got the first user token...')
                asyncio.set_event_loop(asyncio.new_event_loop())
                loop = asyncio.get_event_loop()
                pam_search_results = loop.run_until_complete(__get_os_credential(access_token, host_list, comment))

                if not pam_search_results:
                    logger.info('Login expired, trying to login again...')
                    access_token = __get_token(api_user, api_pw, ldap=True)
                    logger.info('Got the second user token...')
                    pam_search_results = loop.run_until_complete(__get_os_credential(access_token, host_list, comment))

            # Save accounts to Redis
            if pam_search_results:
                cache_accounts = {}
                for result in pam_search_results:
                    host_name = ''
                    for key, value in result.items():
                        if key == 'host_name':
                            host_name = value
                        else:
                            cache_accounts[host_name + '_pam_os_' + key] = value

                # Save host info to Redis, keep 6 hours
                cache.set_many(cache_accounts, 3 * 60 * 60)
        else:
            logger.warning('Not a valid account type.')

    except Exception as e:
        logger.error(api_user + ' error getting pam credential: ' + str(e))
        if e == 403:
            return [{'error': 'Username or password invalid, please correct your username and password and try again'}]
        elif e == 401:
            return [{'error': 'You are not authorized to access this resource, please contact your system administrator'}]
        elif e == 429:
            return [{'error': 'Too many requests, please try again later'}]
        elif e == 500:
            return [{'error': 'Internal server error, please contact your system administrator'}]

    finally:
        if access_token:
            pam_logout(api_user, api_pw, access_token)
            logger.info(api_user + ' logout PAM successful.')

    return pam_search_results + redis_search_results
