# -*- coding: utf-8 -*-
# @Time        : 2024/10/24
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : PMC
# @Project     : GOC Automation Platform
from resource_base.modules.importModules import *
import logging
import requests

# Get the django logger
logger = logging.getLogger('django')


def backup_login():
    url = r'https://banoma.de.bosch.com/loginapi'
    login = {"domain": "BR",
            "username": "AGORCA",
            "password": "TZuI987*!99123654778"}

    response = requests.post(url, json=login, verify=False)

    access_token=''
    if response.status_code == 200:
        response = response.json()
        access_token = response['access_token']

    else:
        logger.error('Error code: ' + str(response.status_code))
        logger.error('Error login backup: ' + str(response.json()))
    
    return access_token


def backup_downtime_schedule(access_token, schedule_id, change_number, server_name, start_time, end_time):

    header = {'Content-Type': 'application/json',
            'Authorization':f'Bearer {access_token}'}

    pmc_schedule = r'https://banoma.de.bosch.com/pmc_schedule'

    #The idea is to do a for loop changing the servername by all affected servers in the PMC, and Backup team check from their side if that is under their control or not
    #Start and End time must be in CET because of UC4 scheduling
    pmc_json = {"pmcid": schedule_id,
    "change": change_number,
    "servername": server_name,
    "starttime": start_time,
    "endtime": end_time}

    response = requests.post(pmc_schedule, json=pmc_json, headers=header, verify=False)
    if response.status_code == 200:
        response = response.json()
        logger.info('Successful scheduled backup downtime: ' + str(response))
        return True
    else:
        logger.error('Error code: ' + str(response.status_code))
        logger.error('Error scheduled backup downtime: ' + str(response.content))
        return False


def backup_schedule_cancel(access_token, schedule_id, change_number):

    header = {'Content-Type': 'application/json',
            'Authorization':f'Bearer {access_token}'}

    pmc_cancel = r'https://banoma.de.bosch.com/pmc_cancel'

    pmc_json = {"pmcid": schedule_id,
    "change": change_number}

    response = requests.post(pmc_cancel, json=pmc_json, headers=header, verify=False)

    if response.status_code == 200:
        response = response.json()
        if schedule_id in response['msg']:
            logger.info('Successful changed backup schedule: ' + response['msg'])
            return True
        else:
            logger.info('Cancel backup schedule failed: ' + response['msg'])
            return False
    else:
        logger.error('Error code: ' + str(response.status_code))
        logger.error('Error cancel backup schedule: ' + str(response.content))
        return False


def backup_schedule_change(access_token, schedule_id, change_number, start_time, end_time):

    header = {'Content-Type': 'application/json',
            'Authorization':f'Bearer {access_token}'}

    pmc_change = r'https://banoma.de.bosch.com/pmc_change'

    pmc_json = {"pmcid": schedule_id,
    "change": change_number,
    "starttime": start_time,
    "endtime": end_time
    }

    response = requests.post(pmc_change, json=pmc_json, headers=header, verify=False)

    if response.status_code == 200:
        response = response.json()
        if schedule_id in response['msg']:
            logger.info('Successful changed backup schedule: ' + response['msg'])
            return True
        else:
            logger.info('Change backup schedule failed: ' + response['msg'])
            return False
    else:
        logger.error('Error code: ' + str(response.status_code))
        logger.error('Error change backup schedule: ' + str(response.content))
        return False
