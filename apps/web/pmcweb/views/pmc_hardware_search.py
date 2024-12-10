# -*- coding: utf-8 -*-
# @Time        : 2023/08/31
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : PMC
# @Project     : GOC Automation Platform

from resource_base.modules.importModules import *
from operationweb.scripts import cmdb_request
from mainweb.models import TimeSavingStatistics
import logging

# Get the django logger
logger = logging.getLogger('django')


def pmc_hardware_search_index(request):
    """Return pmc hardware search page
        Args:
            request
        Returns:
            Render to pmc_hardware_search.html
    """
    return render(request, 'pmc/pmc_hardware_search.html')


def pmc_hardware_search_handle(request):
    """Hardware search
            Args:
                request:
                    hostList: User input host name list
            Returns:
                JsonResponse:
                    search_result: All hardware info for the host list
            """
    # Get the request data
    rec = request.POST
    host_list = rec.get('hostList').split(',')

    # Restrict the number of hosts within 200
    if len(host_list) > 200:
        return JsonResponse({'status': False, 'error': 'Please limit the number of hosts within 200!'})

    logger.info(request.session.get('user_account')['loginid'] + ' is searching hardware info for: %s' % (str(host_list),))

    try:
        # Select the data from CMDB ITCW Standard View
        all_data = cmdb_request.get_hardware_info_from_db(host_list)
    except Exception as e:
        logger.error('Error searching hardware info: ' + str(e))
        return JsonResponse({'status': False, 'error': 'Error searching hardware info: ' + str(e)})

    # Time saving statistic
    TimeSavingStatistics.time_saving_statistic('hardware_search', len(all_data) * 177)
    return JsonResponse({'status': True, 'data': all_data})
