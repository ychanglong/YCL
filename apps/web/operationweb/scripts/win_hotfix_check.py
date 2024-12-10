# -*- coding: utf-8 -*-
# @Time        : 2024/09/05
# @Author      : Wang Gorden (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import winrm,logging, socket
import asyncio
from operationweb.scripts import pam_request

logger = logging.getLogger('django')


# server port 5985 live check
def _connection_test(servername_fqdn):
    connection_status = False
    port_number = 5985

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.connect((servername_fqdn, port_number))
        connection_status = True
    except ConnectionRefusedError:
        connection_status = False
    except socket.timeout:
        connection_status = False
    finally:
        sock.close()

    return connection_status


# 从初始密码列表中筛选出各自的rbadmin_soc或administrator(优先rbadmin_soc,没有就找administrator)
def _raw_credential_account_filter(OSCredentialData):
    OSCredential_packet_dict = {}
    OSCredential_packet_list = []
    OSCredential_list = []

    for item in OSCredentialData:
        tag = item['host_name']
        if tag in OSCredential_packet_dict:
            OSCredential_packet_dict[tag].append(item)
        else:
            OSCredential_packet_dict[tag] = [item]  # 如果发现新host_name 则创建新键值对

    OSCredential_packet_list = list(OSCredential_packet_dict.values())

    found_element = None

    for item_list in OSCredential_packet_list:
        for item in item_list:  # 遍历查找rbadmin_soc
            if 'rbadmin_soc' in item:
                found_element = item
                break

        if found_element is None:  # 如果没有找到rbadmin_soc则再次遍历查找administrator
            for item in item_list:
                if 'administrator' in item:
                    found_element = item
                    break

        OSCredential_list.append(found_element)
        found_element = None

    if (len(OSCredential_packet_list) == len(OSCredential_list)):  # 检查是否获得了全部host的密码
        return OSCredential_list
        # 返回示例: [ {'host_name': 'szhvm00378', 'administrator': 'e98EZW0Q04hHcCG', 'RB_IPAddress': '10.54.12.174'},
        #           {'host_name': 'szhsoc02', 'rbadmin_soc': 'vUtmgY5M76U3Ofz', 'RB_IPAddress': '10.54.12.50'},
        #           {'host_name': 'banvm00078', 'rbadmin_soc': 'rhV54vpJBLPye6i', 'RB_IPAddress': '10.166.150.7'}
        #         ]
    else:
        logger.error('Related credential not found, please run again or check PAM.')


# get OS admin credential (one from rbadmin_soc/administrator) by using pam_request.py
def _get_os_credential(server_list, api_user, api_pw):
    account_type = '2'
    comment = 'test'
    OSCredential_raw = []
    OSCredential_list = []
    host_list = []

    for host in server_list:
        if host.__contains__('.'):
            host_list.append(host.split('.')[0])
        else:
            host_list.append(host)

    OSCredential_raw = pam_request.get_pam_credential(api_user, api_pw, account_type, host_list, comment)
    OSCredential_list = _raw_credential_account_filter(OSCredential_raw)

    # OSCredential_list = [  #{'host_name': 'szhsoc02', 'rbadmin_soc': 'Sjho9So3XNpUX1H', 'RB_IPAddress': '10.54.12.50'}]
    #                         # {'host_name': 'BANVM00078', 'rbadmin_soc': 'kvN5hP34Al2s4Df', 'RB_IPAddress': '10.166.150.7'},
    #                         # {'host_name': 'SZHVM00310', 'administrator': 'JT68nPO64FGtwKt', 'RB_IPAddress': '10.8.136.63'},
    #                         {'host_name': 'si0vm07922 ', 'rbadmin_soc': 'd4gHLUpb08bdSBr', 'RB_IPAddress': '10.73.236.142'}]

    return OSCredential_list
    # 返回格式: [ {'host_name': 'szhsoc02', 'rbadmin_soc': 'Qd3ojqCu7o2JBGP', 'RB_IPAddress': '10.54.12.50'},
    #            {'host_name': 'BANVM00078', 'rbadmin_soc': 'tzP3IxG94WwyJZt', 'RB_IPAddress': '10.166.150.7'} ]


# 获取单台server登陆信息
def _get_single_wimrm_connect_info(OSCredential_list):
    if (len(OSCredential_list) == 1):
        single_wimrm_connect_info = []
        list_single_host = OSCredential_list[0]
        hostname = list_single_host['host_name']
        ip = list_single_host['RB_IPAddress']
        if 'rbadmin_soc' in list_single_host:
            server_account = 'rbadmin_soc'
            server_passwd = list_single_host['rbadmin_soc']
        else:
            server_account = 'administrator'
            server_passwd = list_single_host['administrator']

        single_wimrm_connect_info = [hostname, ip, server_account, server_passwd]

        return single_wimrm_connect_info
    else:
        logger.error(f"ERROR: Not a single OS Credential, please try again.")


def _single_winrm_session_run_ps(ip, server_account, server_passwd, ps_script):
    session = winrm.Session(f"http://{ip}:5985", auth=(f".\{server_account}", server_passwd), transport='ntlm')
    output_raw = session.run_ps(ps_script).std_out
    return output_raw


# asyncio不支持winrm，使用run_in_executor允许在协程中运行阻塞的同步代码
async def _async_winrm_session(url, username, password):
    session = await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: winrm.Session(url, auth=(username, password), transport='ntlm')
    )
    return session

# async run winrm
async def _async_winrm_session_run_ps(ip, server_account, server_passwd, ps_script):
    session = await _async_winrm_session(f"http://{ip}:5985", username=server_account, password=server_passwd)
    run_ps_output = session.run_ps(ps_script).std_out
    return run_ps_output


async def async_run_task(ip, server_account, server_passwd, ps_script):
    run_ps_tasks = []
    task = asyncio.create_task(_async_winrm_session_run_ps(ip, f".\{server_account}", server_passwd, ps_script))
    run_ps_tasks.append(task)
    task_output = await asyncio.wait(run_ps_tasks, timeout=None)

    return task_output


def get_server_uptime_and_hotfix(host_list, api_user, api_pw, action_code):
    # Powershell script need run on remote host
    ps_script_check_uptime = f"""
    $operatingSystem = Get-CimInstance -ClassName Win32_OperatingSystem
    $lastBootUpTime = $operatingSystem.LastBootUpTime
    $uptime = (get-date) - $operatingSystem.LastBootUpTime
    $uptime_days = $uptime.Days

    echo $uptime_days
    """

    # Powershell script for check Win installed hotfix in current and last year
    ps_script_win_get_hotfix = r'''
    $HotFixList = Get-HotFix | Where-Object { $_.InstalledOn.Year -ge ((Get-Date).year - 1)} | Sort-Object -Property InstalledOn
    echo $HotFixList
    '''

    server_uptime = []

    try:

        # PAM取密码
        OSCredential_list = _get_os_credential(host_list, api_user, api_pw)

        # action_code等于(str)1时，检查host列表中所有服务器的uptime
        if action_code == '1':
            server_uptime = OSCredential_list

            for hostinfo in server_uptime:
                host_info = []
                host_info.append(hostinfo)  # {}变成[{}],统一格式，方便函数处理
                single_wimrm_connect_info = _get_single_wimrm_connect_info(host_info)
                # host = single_wimrm_connect_info[0]
                ip = single_wimrm_connect_info[1]
                server_account = single_wimrm_connect_info[2]
                server_passwd = single_wimrm_connect_info[3]

                if _connection_test(ip):  # 检测ip:5985是否有响应

                    uptime_raw = asyncio.run(async_run_task(ip, server_account, server_passwd, ps_script_check_uptime))

                    # str处理出所需部分
                    uptime_day = str(uptime_raw).split("b'")[1].split("\\r\\n")[0]

                    if uptime_day == '0' or uptime_day == '1':
                        hostinfo.update({'uptime': uptime_day + ' Day'})
                    else:
                        hostinfo.update({'uptime': uptime_day + ' Days'})

                else:
                    hostinfo.update({'uptime': 'Not available.'})
                    logger.error("Server not available or not in BCN or not a Windows, please check server.")

            return server_uptime
            # 返回格式: [{'host_name': 'SZHVM00310', 'administrator': 'JT68nPO64FGtwKt', 'RB_IPAddress': '10.8.136.63', 'uptime': '23 Days'},
            #          {'host_name': 'si0vm07922 ', 'rbadmin_soc': 'OjYdtZA9q17rlKY', 'RB_IPAddress': '10.73.236.142', 'uptime': '1 Day'}]

        # action_code等于(str)2时，列出当前服务器(单台)最近两年内安装过的hotfix
        if action_code == '2':
            hotfix_list = OSCredential_list

            for hostinfo in hotfix_list:
                host_info = []
                host_info.append(hostinfo)  # {}变成[{}],统一格式，方便函数处理
                single_wimrm_connect_info = _get_single_wimrm_connect_info(host_info)
                # host = single_wimrm_connect_info[0]
                ip = single_wimrm_connect_info[1]
                server_account = single_wimrm_connect_info[2]
                server_passwd = single_wimrm_connect_info[3]

                if _connection_test(ip):  # 检测ip:5985是否有响应
                    hotfix_list_raw = _single_winrm_session_run_ps(ip, server_account, server_passwd, ps_script_win_get_hotfix)
                    hotfix_list_str = str(hotfix_list_raw).replace(r'\r\n', '\n').split("'")[1].strip()

                    hostinfo.update({'hotfix_list': hotfix_list_str})
                else:
                    hostinfo.update({'hotfix_list': 'Not available.'})
                    logger.error("Server not available or not in BCN or not a Windows, please check server.")

            return hotfix_list  # 返回值带密码
            # 返回示例: [{'host_name': 'BANVM00078', 'rbadmin_soc': 'tzP3IxG94WwyJZt', 'RB_IPAddress': '10.166.150.7', 'hotfix_list': 'Source        Description      HotFixID      InstalledBy          InstalledOn              \n------        -----------      --------      -----------          -----------              \nBANVM00078    Security Update  KB5034862     NT AUTHORITY\\\\SYSTEM  2/15/2024 12:00:00 AM    \nBANVM00078    Security Update  KB5034767     NT AUTHORITY\\\\SYSTEM  2/24/2024 12:00:00 AM    \nBANVM00078    Update           KB5034614     NT AUTHORITY\\\\SYSTEM  2/24/2024 12:00:00 AM    \nBANVM00078    Security Update  KB5035962     NT AUTHORITY\\\\SYSTEM  3/13/2024 12:00:00 AM    \nBANVM00078    Security Update  KB5037016     NT AUTHORITY\\\\SYSTEM  4/10/2024 12:00:00 AM'}]

    except Exception as e:
        logger.error(f"Error: check server failed, please try again." + str(e))


# servername = r'xxx'
# api_user = r'test'
# api_pw = r'test'
#
# result = get_server_uptime_and_hotfix(servername, api_user, api_pw, '1')
# print(result)
