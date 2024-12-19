# -*- coding: utf-8 -*-
# @Time        : 2023/12/27
# @Author      : WANG Gorden (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import subprocess
import winrm,logging, socket
from operationweb.scripts import pam_request

logger = logging.getLogger('django')


# get server ip
def get_ip(servername_fqdn):
    ip = socket.gethostbyname(servername_fqdn)
    return ip


# server port 5985 live check
def connection_test(servername_fqdn):
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


# get OS admin credential (one from rbadmin_soc/rbadmin/administrator) by using pam_request.py
def get_os_credential(servername, api_user, api_pw):

    OSCredential = []
    AccountFound = False

    hostname = []
    if servername.__contains__('.'):
        hostname.append(servername.split('.')[0])
    else:
        hostname.append(servername)
    comment = 'automation_os_service_check'

    try:
        OSCredentialData = pam_request.get_pam_credential(api_user, api_pw, '2', hostname, comment)

        for item in OSCredentialData:
            if 'rbadmin_soc' in item:
                key = 'rbadmin_soc'
                value = item['rbadmin_soc']
                break
            elif 'rbadmin' in item:
                key = 'rbadmin'
                value = item['rbadmin']
                break
            elif 'administrator' in item:
                key = 'administrator'
                value = item['administrator']
                break

        if 'key' in locals() and 'value' in locals():
            AccountFound = True
            OSCredential = [key, value]
        else:
            logger.error('No available account.')

        return OSCredential

    except Exception as e:
        logger.error(f"Error: get OS credential failed, please try again." + str(e))


def get_service_status(servername_fqdn, ip, service_name, server_account, server_passwd):

    # service_status = [servername_fqdn, service_name, servicestatus, servicestarttype]
    service_status = [servername_fqdn, service_name]

    try:
        # ip = get_ip(servername_fqdn)

        # Powershell script need run on remote host
        ps_script = f"""
            $serviceInfo = Get-Service -Name {service_name}
            $serviceStatus = $serviceInfo.Status
            $startup_type = $serviceInfo.StartType
            echo $serviceStatus,$startup_type
            """
        session = winrm.Session(fr'http://{ip}:5985', auth=('.'+'\\'+server_account, server_passwd), transport='ntlm')
        response = session.run_ps(ps_script)
        service_status_raw_byte = response.std_out

        # byte to str and split
        service_status_raw_str = str(service_status_raw_byte, encoding='utf-8')
        service_status_out = service_status_raw_str.splitlines()

        service_status.append(service_status_out[0])
        service_status.append(service_status_out[1])

        return service_status
    except Exception as e:
        logger.error(f"Error: check service status failed, please try again." + str(e))


def restart_service(servername_fqdn, ip, service_name, server_account, server_passwd):
    # restart_service_result = ['szhsoc02.apac.bosch.com', 'w32time', 'Running', 'success/failed']
    restart_service_result = [servername_fqdn, service_name]

    try:
        # Powershell script: restart service and check status
        ps_script = f"""
            Stop-Service -Name {service_name} -Force
            # Set-Service -Name {service_name} -StartupType Automatic
            Start-Sleep -Seconds 1
            
            $serviceInfo = Get-Service -Name {service_name}
            $serviceStatus = $serviceInfo.Status
            echo $serviceStatus
            
            Start-Service -Name {service_name} -Force
            Start-Sleep -Seconds 2
            
            $serviceInfo = Get-Service -Name {service_name}
            $serviceStatus = $serviceInfo.Status
            echo $serviceStatus
            """
        session = winrm.Session(fr'http://{ip}:5985', auth=('.'+'\\'+server_account, server_passwd), transport='ntlm')

        response = session.run_ps(ps_script)
        # response = session.run_ps(ps_script, elevate=True)
        service_status_raw_byte = response.std_out

        # byte to str and split
        service_status_raw_str = str(service_status_raw_byte, encoding='utf-8')
        service_status_out = service_status_raw_str.splitlines()

        if (service_status_out[0] == 'Stopped' and service_status_out[1] == 'Running'):
            restart_service_status = 'success'
        else:
            restart_service_status = 'failed'

        restart_service_result.append(service_status_out[1])
        restart_service_result.append(restart_service_status)

        return restart_service_result
    except Exception as e:
        logger.error(f"Error: restart service failed, please try again." + str(e))


# operation_tag: 1-get_service_status; 2-restart_service
def windows_service_check(servername_fqdn, api_user, api_pw, service_name, operation_tag):

    try:
        servername_fqdn = servername_fqdn.lower()
        # if server port 5985 available:
        if connection_test(servername_fqdn) == False:
            logger.error("Server not available or not in BCN or not a Windows, please check again.")
        else:
            # get ip
            ip = get_ip(servername_fqdn)

            # get hostname
            if servername_fqdn.__contains__('.'):
                hostname = servername_fqdn.split('.')[0]
            else:
                hostname = servername_fqdn

            # get_os_credential()
            server_credential = get_os_credential(hostname, api_user, api_pw)
            # error:get server credential failed.
            server_account = server_credential[0]
            server_passwd = server_credential[1]

            if operation_tag == '1':
                service_status = get_service_status(servername_fqdn, ip, service_name, server_account, server_passwd)
                return service_status

            elif operation_tag == '2':
                service_restart_status = restart_service(servername_fqdn, ip, service_name, server_account, server_passwd)
                return service_restart_status
            else:
                logger.error(f"Wrong operation command, please try again.")
    except Exception as e:
        logger.error(f"Error: check/restart service failed, please try again." + str(e))
