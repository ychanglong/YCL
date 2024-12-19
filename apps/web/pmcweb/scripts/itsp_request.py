# -*- coding: utf-8 -*-
# @Time        : 2023/06/07
# @Author      : Wang Gorden (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : PMC Tools
# @Project     : GOC Automation Platform

import requests
import logging
from requests_ntlm import HttpNtlmAuth
import xml.etree.ElementTree as ET

logger = logging.getLogger('django')

# get data by URL, example ID:20007770
def __servicecatalog_get_requisition(itsp_number, ntaccount, ntpassword):
    ret = None
    try:
        session = requests.Session()
        # Example: HttpNtlmAuth('apac\\test','testpass')
        # session.auth = HttpNtlmAuth(r"%s"%ntaccount, ntpassword)
        session.auth = HttpNtlmAuth(ntaccount, ntpassword)
        ret = session.get(
            'https://rb-servicecatalog.apps.intranet.bosch.com/RequestCenter/nsapi/transaction/requisitions/id/' + itsp_number + '/requisitiondata',
            verify=False)

        # check response
        response = ret.text

        if response.__contains__('401 - Unauthorized'):
            ret = '401'
        elif response.__contains__('403 - Forbidden: Access is denied'):
            ret = '403'
        elif response.__contains__('404 - File or directory not found'):
            ret = '404'

    except Exception as e:
        logger.error("Error retrieving ITSP data: " + str(e))

    return ret

# main: get ITSP data and return with dic
def get_itsp_data(itsp_number, ntaccount, ntpassword):
    result = __servicecatalog_get_requisition(itsp_number, ntaccount, ntpassword)

    if result == '401':
        logger.error("Error: Access ITSP API failed, please check your credential.")
        return "401"
    elif result == "403":
        logger.error("Error: Access ITSP API denied, please check your role.")
        return "403"
    elif result == "404":
        logger.error("Error: ITSP number not exist, please check again.")
        return "404"
    else:
        root = ET.fromstring(result.text)

        itsp_data = {}

        for FormField in root.iter('FormField'):
            for child in FormField:
                if child.tag == 'CI_ADD_CHANGE_DELETE.AddChangeDelete':
                    if child.text is None:
                        itsp_data['dataCenterRoom'] = ''
                    else:
                        itsp_data['dataCenterRoom'] = child.text.strip()
                elif child.tag == 'CI_SUPPORT_INFORAMTION.levelname':
                    if child.text is None:
                        itsp_data['change_class'] = ''
                    else:
                        itsp_data['change_class'] = child.text.strip()
                elif child.tag == 'CI_GROWTH.Simultaneous_Users':
                    if child.text is None:
                        itsp_data['reason'] = ''
                    else:
                        itsp_data['reason'] = child.text.strip()
                elif child.tag == 'CMN_DATES_TIMES.Date1':
                    if child.text is None:
                        itsp_data['start_date'] = ''
                    else:
                        itsp_data['start_date'] = child.text.strip()
                elif child.tag == 'CI_DATABASE_BACKUPTIME.Backuptime':
                    if child.text is None:
                        itsp_data['start_time'] = ''
                    else:
                        itsp_data['start_time'] = child.text.strip()
                elif child.tag == 'CI_DATABASE_DELITION.DateofDelition':
                    if child.text is None:
                        itsp_data['end_date'] = ''
                    else:
                        itsp_data['end_date'] = child.text.strip()
                elif child.tag == 'CI_FREE_TEXT_ORDER.Free':
                    if child.text is None:
                        itsp_data['end_time'] = ''
                    else:
                        itsp_data['end_time'] = child.text.strip()
                elif child.tag == 'CI_SERV_OPTIONS.AddRAM_A':
                    if child.text is None:
                        itsp_data['start_with_shutdown'] = ''
                    else:
                        itsp_data['start_with_shutdown'] = child.text.strip()
                elif child.tag == 'CI_SERV_OPTIONS.AppDAS_A':
                    if child.text is None:
                        itsp_data['region'] = ''
                    else:
                        itsp_data['region'] = child.text.strip()
                elif child.tag == 'CI_SERV_OPTIONS.NumbDAS_DISKS_A':
                    if child.text is None:
                        itsp_data['location_code'] = ''
                    else:
                        itsp_data['location_code'] = child.text.strip()
                elif child.tag == 'CI_SERV_OPTIONS.SizDAS_DISKS_A':
                    if child.text is None:
                        itsp_data['additional_people'] = ''
                    else:
                        itsp_data['additional_people'] = child.text.strip()
                elif child.tag == 'Approving_Dso_Basic_en.Select_Person':
                    if child.text is None:
                        itsp_data['people_onsite'] = ''
                    else:
                        itsp_data['people_onsite'] = child.text.strip()
                elif child.tag == 'Approving_Dso_Basic_en.Email_Address':
                    if child.text is None:
                        itsp_data['email_address'] = ''
                    else:
                        itsp_data['email_address'] = child.text.strip()
                elif child.tag == 'CI_WAN_ISP.ISPName':
                    if child.text is None:
                        itsp_data['contact_information'] = ''
                    else:
                        itsp_data['contact_information'] = child.text.strip()

        itsp_data['pmc_start_time'] = itsp_data['start_date'] + ' ' + itsp_data['start_time'] + ':00'
        itsp_data['pmc_end_time'] = itsp_data['end_date'] + ' ' + itsp_data['end_time'] + ':00'

        return itsp_data
