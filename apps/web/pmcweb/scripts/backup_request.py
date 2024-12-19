# -*- coding: utf-8 -*-
# @Time        : 2024/10/24
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : PMC
# @Project     : GOC Automation Platform
from resource_base.modules.importModules import *
from mainweb.models import APIVisitStatistics
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
    
    # API requests statistics
    APIVisitStatistics.save_api_requests('BACKUP', url, 1)
    
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

    logger.info("Backup schedule request: " + str(pmc_json))

    response = requests.post(pmc_schedule, json=pmc_json, headers=header, verify=False)

    # API requests statistics
    APIVisitStatistics.save_api_requests('BACKUP', pmc_schedule, 1)

    if response.status_code == 200:
        response = response.json()
        logger.info('Successful scheduled backup downtime: ' + str(response))
        return True
    else:
        logger.error('Error code: ' + str(response.status_code))
        logger.error('Error scheduling backup downtime: ' + str(response.content))
        return False


def backup_schedule_cancel(access_token, schedule_id, change_number):

    header = {'Content-Type': 'application/json',
            'Authorization':f'Bearer {access_token}'}

    pmc_cancel = r'https://banoma.de.bosch.com/pmc_cancel'

    pmc_json = {"pmcid": schedule_id,
    "change": change_number}

    response = requests.post(pmc_cancel, json=pmc_json, headers=header, verify=False)

    # API requests statistics
    APIVisitStatistics.save_api_requests('BACKUP', pmc_cancel, 1)

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
        logger.error('Error canceling backup schedule: ' + str(response.content))
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

    # API requests statistics
    APIVisitStatistics.save_api_requests('BACKUP', pmc_change, 1)

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
        logger.error('Error changing backup schedule: ' + str(response.content))
        return False


def backup_schedule_close(access_token, schedule_id, change_number):
    
    header = {'Content-Type': 'application/json',
            'Authorization':f'Bearer {access_token}'
             }
    
    pmc_close = r'https://banoma.de.bosch.com/pmc_close'

    pmc_json = {"pmcid": schedule_id,
                "change": change_number}

    response = requests.post(pmc_close, json=pmc_json, headers=header, verify=False)

    # API requests statistics
    APIVisitStatistics.save_api_requests('BACKUP', pmc_close, 1)
    
    if response.status_code == 200:
        response = response.json()
        if schedule_id in response['msg']:
            logger.info('Successful close backup schedule: ' + response['msg'])
            return True
        else:
            logger.info('Close backup schedule failed: ' + response['msg'])
            return False
    else:
        logger.error('Error code: ' + str(response.status_code))
        logger.error('Error closing backup schedule: ' + str(response.content))
        return False
