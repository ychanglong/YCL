# -*- coding: utf-8 -*-
# @Time        : 2023/05/17
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from operationweb.scripts import cmdb_request
from mainweb.models import TimeSavingStatistics
import logging

# Get the django logger
logger = logging.getLogger('django')


def cmdb_search_index(request):
    return render(request, 'operation/cmdb_search.html')


def cmdb_search_handle(request):
    """CMDB search
        Args:
            request:
                hostList: User input host name list
        Returns:
            JsonResponse:
                search_result: All hosts info for the host list
        """
    # Get the request data
    rec = request.POST
    host_list = rec.get('hostList').split(',')

    # Restrict the number of hosts within 2000
    if len(host_list) > 2000:
        return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 2000!'})

    # Get the selected attributes and stored into a dict
    select_attributes_dict = {'name': rec.get('CIName'), 'tier_2': rec.get('CIType'), 'status': rec.get('status'),
                              'status_reason': rec.get('statusReason'), 'dutyclass': rec.get('dutyClass'),
                              'networkconnection': rec.get('securityZone'), 'baselineci': rec.get('baselineCI'),
                              'serial_number': rec.get('serialNumber'), 'datacenterroom': rec.get('managedLocation'),
                              'os_backup_required': rec.get('osBackupRequired'), 'used_by': rec.get('usedBy'),
                              'po_orgunit_name': rec.get('masterOfSystem'), 'fsx_contact': rec.get('fsxContact'),
                              'fsx_contact_email': rec.get('fsxContactEmail'), 'ilo_ip': rec.get('iLOIP')}

    logger.info(request.session.get('user_account')['loginid'] + ' is searching CMDB for: %s' % (str(host_list),))

    try:
        # Select the data from CMDB ITCW Standard View
        all_data = cmdb_request.get_data_from_db(host_list, select_attributes_dict)
    except Exception as e:
        logger.error('Error searching CMDB: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error searching CMDB: ' + str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('cmdb_search', len(all_data) * 177)
    return JsonResponse({'status': True, 'data': all_data})
