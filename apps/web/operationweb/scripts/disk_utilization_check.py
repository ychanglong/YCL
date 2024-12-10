# -*- coding: utf-8 -*-
# @Time        : 2024/04/24
# @Author      : WANG Gorden (BD/ISA-GOC6)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Disk utilization check
# @Project     : GOC Automation Platform


import asyncio
import winrm
import socket, logging
from operationweb.scripts import pam_request


logger = logging.getLogger('django')


# 检查server的5985端口是否可达
def _connection_test(ip):
    connection_status = False
    port_number = 5985

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)

    try:
        sock.connect((ip, port_number))
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
            server_account = '.\\' + 'rbadmin_soc'
            server_passwd = list_single_host['rbadmin_soc']
        else:
            server_account = '.\\' + 'administrator'
            server_passwd = list_single_host['administrator']

        single_wimrm_connect_info = [hostname, ip, server_account, server_passwd]

        return single_wimrm_connect_info
    else:
        logger.error(f"ERROR: Not a single OS Credential, please try again.")


def _single_winrm_session_run_ps(ip, server_account, server_passwd, ps_script):
    session = winrm.Session(f"http://{ip}:5985", auth=(server_account, server_passwd), transport='ntlm')
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
    task = asyncio.create_task(_async_winrm_session_run_ps(ip, server_account, server_passwd, ps_script))
    run_ps_tasks.append(task)
    task_output = await asyncio.wait(run_ps_tasks, timeout=None)

    return task_output


# action_code：‘1’-返回C盘可用空间;'2'-清理C盘并返回释放出的空间大小和清理后的C盘可用空间;'3'-列出C盘根目录下文件和文件夹大小
def disk_utilization_check(host_list, api_user, api_pw, action_code):
    # Powershell script for check free space of disk C
    ps_script_check_c = r"""
    $strLogicDiskC = Get-WMIObject Win32_LogicalDisk | Where-Object {$_.DeviceID -eq "c:"}
    $GB = 1073741824
    $fltDiskCFreeGB = $strLogicDiskC.FreeSpace /$GB
    echo $fltDiskCFreeGB
    """

    # Powershell script for clean recycle bin and temp folder in disk C
    ps_script_check_and_clean_c = r"""
    #clean temp folders and recycle bin
    $strLogicDiskC = Get-WMIObject Win32_LogicalDisk | Where-Object {$_.DeviceID -eq "c:"}
    $GB = 1073741824
    $flt_DiskCFreeGB = $strLogicDiskC.FreeSpace /$GB

    Clear-RecycleBin -Force -DriveLetter C:
    #Get-ChildItem -Path C:\temp\ -Recurse | Remove-Item -force -recurse
    #Get-ChildItem -Path C:\Windows\Temp -Recurse | Remove-Item -force -recurse

    #check free space after clean
    $strLogicDiskC_afterClean = Get-WMIObject Win32_LogicalDisk | Where-Object {$_.DeviceID -eq "c:"}
    $flt_DiskCFreeGB_afterClean = $strLogicDiskC_afterClean.FreeSpace /$GB

    $flt_Freeed_space = $flt_DiskCFreeGB_afterClean - $flt_DiskCFreeGB
    echo $flt_Freeed_space
    echo $flt_DiskCFreeGB_afterClean
    """

    # Powershell script for list size of folders and files in disk C
    ps_script_list_file_size = r"""
    #$TargetPath = 'C:\Program Files'
    $TargetPath = 'C:\'

    Get-ChildItem -Path $TargetPath -ErrorAction SilentlyContinue -Force |
    Format-Table  -AutoSize LastWriteTime, Name,
         @{ Label="Length"; alignment="Left";
           Expression={
                        if($_.PSIsContainer -eq $True)
                            {$foldersize = (New-Object -com  Scripting.FileSystemObject).GetFolder( $_.FullName).Size
                             "$([math]::round($foldersize / 1GB, 3))GB"}
                        else
                            {"$([math]::round($_.Length / 1GB, 3))GB"}
                      }
         };
    """

    OSCredential_list = []

    try:

        # PAM取密码
        OSCredential_list = _get_os_credential(host_list, api_user, api_pw)
        # OSCredential_list = [{'host_name': 'BANVM00078', 'rbadmin_soc': 'DfNkBD1lS1D5aZv', 'RB_IPAddress': '10.166.150.7'}]

        # action_code等于(str)1时，检查host列表中所有服务器C盘的可用空间
        if action_code == '1':
            check_space_c_list_result = OSCredential_list

            for hostinfo in check_space_c_list_result:
                host_info = []
                host_info.append(hostinfo)  # {}变成[{}],统一格式，方便函数处理
                single_wimrm_connect_info = _get_single_wimrm_connect_info(host_info)
                # host = single_wimrm_connect_info[0]
                ip = single_wimrm_connect_info[1]
                server_account = single_wimrm_connect_info[2]
                server_passwd = single_wimrm_connect_info[3]

                if _connection_test(ip):  # 检测ip:5985是否有响应

                    c_space_raw = asyncio.run(async_run_task(ip, server_account, server_passwd, ps_script_check_c))

                    # str处理出所需部分
                    c_space = round(float(str(c_space_raw).split("b'")[1].split("\\r\\n")[0]), 2)

                    hostinfo.update({'free_space_c': str(c_space) + 'GB'})

                else:
                    hostinfo.update({'free_space_c': 'Not available.'})
                    logger.error("Server not available or not in BCN or not a Windows, please check server.")

            return check_space_c_list_result
            # 返回示例:[  {'host_name': 'szhsoc02', 'rbadmin_soc': 'AoOwUqjuS5vc60P', 'RB_IPAddress': '10.54.12.50', 'free_space_c': '24.42GB'},
            #           {'host_name': 'SZHVM00310', 'administrator': 'xTpK8P6tR3vV29h', 'RB_IPAddress': '10.8.136.63', 'free_space_c': '37.66GB'}
            #         ]

            # action_code等于(str)2时，清理单台server中C盘的回收站和temp文件夹
        elif action_code == '2':
            cleaned_c_space_result = OSCredential_list

            single_wimrm_connect_info = _get_single_wimrm_connect_info(OSCredential_list)
            host = single_wimrm_connect_info[0].lower()
            ip = single_wimrm_connect_info[1]
            server_account = single_wimrm_connect_info[2]
            server_passwd = single_wimrm_connect_info[3]

            if _connection_test(ip):  # 检测ip:5985是否有响应

                check_and_clean_raw = asyncio.run(async_run_task(ip, server_account, server_passwd, ps_script_check_and_clean_c))

                clean_and_check_result_list = str(check_and_clean_raw).split("b'")[1].split("\\r\\n")
                logger.info(clean_and_check_result_list)
                freed_space = round(float(clean_and_check_result_list[0]), 2)
                free_space_c_after_clean = round(float(clean_and_check_result_list[1]), 2)

                cleaned_c_space_result[0].update({'freed_space': str(freed_space) + 'GB'})
                cleaned_c_space_result[0].update({'free_space_c_after_clean': str(free_space_c_after_clean) + 'GB'})
            else:
                cleaned_c_space_result[0].update({'freed_space': 'Not available.'})
                cleaned_c_space_result[0].update({'free_space_c_after_clean': 'Not available.'})

                logger.error("Server not available or not in BCN or not a Windows, please check server.")

            return cleaned_c_space_result
            # 返回示例:[{'host_name': 'szhsoc02', 'rbadmin_soc': 'AoOwUqjuS5vc60P', 'RB_IPAddress': '10.54.12.50', 'freed_space': '0.2GB', 'free_space_c_after_clean': '24.42GB'}]

        # action_code等于3时，列出C盘各文件和文件夹的大小(Windows文件夹除外)
        elif action_code == '3':
            file_size_list_result = []

            single_wimrm_connect_info = _get_single_wimrm_connect_info(OSCredential_list)
            host = single_wimrm_connect_info[0].lower()
            ip = single_wimrm_connect_info[1]
            server_account = single_wimrm_connect_info[2]
            server_passwd = single_wimrm_connect_info[3]

            if _connection_test(ip):
                # session = winrm.Session(fr'http://{ip}:5985', auth=(server_account, server_passwd), transport='ntlm')
                # file_size_list_raw = session.run_ps(ps_script_list_file_size).std_out

                file_size_list_raw = _single_winrm_session_run_ps(ip, server_account, server_passwd, ps_script_list_file_size)

                # format output:
                file_size_list = str(file_size_list_raw).replace(r'\r\n', '\n').split("'")[1].strip()
                file_size_list_result.append({host: file_size_list})
            else:
                file_size_list_result.append({host: 'Not available.'})

                logger.error("Server not available or not in BCN or not a Windows, please check server.")

            return file_size_list_result
            # 返回示例:[{'SZHVM00310': 'LastWriteTime          Name                      Length  \n-------------          ----                      ------  \n11/7/2023 9:37:42 PM   $Recycle.Bin              0GB     \n5/28/2020 4:51:15 PM   Automic                   0.165GB \n2/25/2024 11:47:41 AM  Config.Msi                0GB     \n5/28/2020 8:17:23 AM   Documents and Settings    0GB     \n1/11/2021 10:59:26 AM  inetpub                   0.151GB \n5/15/2020 8:19:21 PM   PerfLogs                  0GB     \n11/26/2023 11:02:27 AM Program Files             7.013GB \n12/12/2022 1:31:27 PM  Program Files (x86)       1.03GB'}]
        else:
            logger.error(f"action code not in scope, please correct and try again.")
    except Exception as e:
        logger.error(f"Error: disk utilization check failed, please try again." + str(e))

