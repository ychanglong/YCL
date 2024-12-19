# -*- coding: utf-8 -*-
# @Time        : 2023/05/17
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Operation Tools
# @Project     : GOC Automation Platform

import oracledb
import logging
import re
from mainweb.models import APIVisitStatistics

# Get the django logger
logger = logging.getLogger('django')

def __sql_stitching(host_list, select_attributes_dict):
    # Initiate some varibles
    sql = "SELECT "
    v_rel_acc_join = False
    v_rel_org_join = False

    # If the used_by attribute selected
    if select_attributes_dict['used_by']:
        v_rel_acc_join = True
    # If the master of system attribute selected
    if select_attributes_dict['po_orgunit_name']:
        v_rel_org_join = True

    for attribute, value in select_attributes_dict.items():
        if not v_rel_acc_join and not v_rel_org_join:
            if value:
                sql += (attribute + ',')
        else:
            if value:
                if attribute != 'used_by' and attribute != 'po_orgunit_name':
                    sql += ('a.' + attribute + ',')
                elif attribute == 'used_by':
                    sql += 'b.email_address,'
                elif attribute == 'po_orgunit_name':
                    sql += 'c.po_orgunit_name,'
                else:
                    continue

    sql = sql[:-1]

    if not v_rel_acc_join and not v_rel_org_join:
        sql += ' FROM cmswhs.v_spl_h_item WHERE name IN ('
    elif v_rel_acc_join and v_rel_org_join:
        sql += ' FROM cmswhs.v_spl_h_item a inner join cmswhs.v_spl_v_rel_acc b on a.itcw_ref_id = b.itcw_ref_id inner join cmswhs.v_spl_v_rel_org c on a.itcw_ref_id = c.itcw_ref_id WHERE name IN ('
    elif v_rel_acc_join and not v_rel_org_join:
        sql += ' FROM cmswhs.v_spl_h_item a inner join cmswhs.v_spl_v_rel_acc b on a.itcw_ref_id = b.itcw_ref_id WHERE name IN ('
    else:
        sql += ' FROM cmswhs.v_spl_h_item a inner join cmswhs.v_spl_v_rel_org c on a.itcw_ref_id = c.itcw_ref_id WHERE name IN ('

    for host in host_list:
        sql += ("'" + host.upper() + "',")

    sql = sql[:-1] + ')'

    logger.info('Executing SQL: ' + sql)

    return sql


def __convert_db_results(cursor, results):
    list_result = []
    for i in results:
        list_list = list(i)
        des = cursor.description  # 获取表详情，字段名，长度，属性等

        t = ",".join([item[0] for item in des])
        table_head = t.split(',')  # # 查询表列名 用,分割

        dict_result = dict(zip(table_head, list_list))  # 打包为元组的列表 再转换为字典

        list_result.append(dict_result)  # 将字典添加到list_result中

    return list_result


def isIP(str):
    p = re.compile('^((25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(25[0-5]|2[0-4]\d|[01]?\d\d?)$')
    if p.match(str):
        return True
    else:
        return False


def __get_storage_device_list_from_db(connection, data_center_room_list):

    # Create cursor
    cursor = connection.cursor()

    try:
        sql = """select

                    name as ci_name
                    ,type_name as ci_type
                    ,status_reason
                    ,tier_2
                    ,tier_3
                    ,primary_support_group
                    ,datacenterroom as dcr

                    from
                        cmswhs.v_spl_h_item

                    where
                    datacenterroom in ({})

                    and status = 'Deployed'
                    and status_reason = 'Productive'
                    and tier_1 = 'Infrastructure'
                    and tier_2 = 'Storage'

                    and primary_support_group in ('Storage Services','SAN Services','File Services','File Services Americas','Operations Regional Storage AP')
        """.format(str(data_center_room_list).strip('[]'))

        cursor.execute(sql)

        results = cursor.fetchall()

        list_result = __convert_db_results(cursor, results)

        nas_cluster_dict = {}

        for storage_item in list_result:
            if storage_item['TIER_3'] == 'NAS Storage System':
                nas_cluster = storage_item['CI_NAME'].split('-')[0]
                if storage_item['DCR'] not in nas_cluster_dict.keys():
                    nas_cluster_dict[storage_item['DCR']] = []
                nas_cluster_dict[storage_item['DCR']].append(nas_cluster)

        for key, value in nas_cluster_dict.items():
            nas_cluster_dict[key] = list(set(value))

        for dcr, nas_clusters in nas_cluster_dict.items():
            for cluster in nas_clusters:
                list_result.append(
                    {'CI_NAME': cluster, 'CI_TYPE': 'Cluster', 'STATUS_REASON': 'Productive', 'TIER_2': 'Storage',
                     'TIER_3': 'NAS Storage System', 'PRIMARY_SUPPORT_GROUP': 'Operations Regional Storage AP',
                     'DCR': dcr})

        for device_item in list_result:
            device_item['ILO_IP'] = ''
            device_item['VCENTER'] = ''

        return list_result

    except Exception as e:
        logger.error('Error getting storage device list: ' + str(e))
    finally:
        # Close the cursor
        cursor.close()
        # API requests statistics
        APIVisitStatistics.save_api_requests('CMDB', 'rb0orarac34.de.bosch.com', len(data_center_room_list))


def __get_server_device_list_from_db(connection, data_center_room_list):

    # Create cursor
    cursor = connection.cursor()

    try:
        sql_1 = """select

                a.name as ci_name
                ,a.type_name as ci_type
                ,a.status_reason
                ,a.tier_2
                ,a.tier_3
                ,a.primary_support_group
                ,a.datacenterroom as dcr
                ,a2.name as ilo_ip

                from
                    cmswhs.v_spl_h_item a

                    left outer JOIN cmswhs.v_spl_v_rel_i2i     s ON a.itcw_ref_id = s.itcw_ref_id_child
                    left outer JOIN cmswhs.v_spl_h_item       a2 ON s.itcw_ref_id_parent = a2.itcw_ref_id

                where
                a.datacenterroom in ({})
                and a.type_name = 'Computer System'
                and a.status = 'Deployed'
                and a.status_reason = 'Productive'
                and a.tier_1 = 'Server'
                and a.tier_2 = 'Hardware'
                and a.tier_3 = 'X86 certified Hardware'
                and a.primary_support_group in ('External Server Support','x86 Hardware Operation','ESX Server Service')

        """.format(str(data_center_room_list).strip('[]'))

        cursor.execute(sql_1)

        results = cursor.fetchall()

        # Add tittle to the results list
        convert_db_result = __convert_db_results(cursor, results)

        sorted_device_dict = {}
        for device_item in convert_db_result:
            if device_item['CI_NAME'] not in sorted_device_dict.keys():
                if isIP(device_item['ILO_IP']):
                    sorted_device_dict[device_item['CI_NAME']] = device_item
                else:
                    sorted_device_dict[device_item['CI_NAME']] = device_item
                    sorted_device_dict[device_item['CI_NAME']]['ILO_IP'] = ''
            else:
                if sorted_device_dict[device_item['CI_NAME']]['ILO_IP'] == '':
                    if isIP(device_item['ILO_IP']):
                        sorted_device_dict[device_item['CI_NAME']]['ILO_IP'] = device_item['ILO_IP']
                    else:
                        continue
                else:
                    continue

        list_result = list(sorted_device_dict.values())

        # Query for vCenter information
        esx_list = []
        for device_item in list_result:
            if 'VMH' in device_item['CI_NAME']:
                esx_list.append(device_item['CI_NAME'])

        vcenter_info_dict = {}
        cluster_info_dict = {}

        # If ESX exist in DCR
        if esx_list:
            sql_2 = """select distinct
                a2.name as child_name
                ,a2.tier_3 as child_tier_3
                ,a2.dnsdomain as child_dnsdomain
                ,a3.name as parent_name
                ,a3.tier_3 as parent_tier_3
    
                from
                cmswhs.v_spl_h_item a
    
                left outer JOIN cmswhs.v_spl_v_rel_i2i      s ON a.itcw_ref_id = s.itcw_ref_id_child
                left outer JOIN cmswhs.v_spl_h_item        a2 ON s.itcw_ref_id_parent = a2.itcw_ref_id
    
                left outer JOIN cmswhs.v_spl_v_rel_i2i     s ON a.itcw_ref_id = s.itcw_ref_id_parent
                left outer JOIN cmswhs.v_spl_h_item        a3 ON s.itcw_ref_id_child = a3.itcw_ref_id
    
                where
                a3.name in (select
                    a2.name
                    from
                        cmswhs.v_spl_h_item a
                        left outer JOIN cmswhs.v_spl_v_rel_i2i     s ON a.itcw_ref_id = s.itcw_ref_id_parent
                        left outer JOIN cmswhs.v_spl_h_item       a2 ON s.itcw_ref_id_child = a2.itcw_ref_id
                    where
                    a.name in ({})
                    and a2.tier_3 = 'Vmware ESX Cluster')
                and (a2.tier_3 = 'Application Instance' or a2.tier_3 = 'Vmware ESX Server')
    
            """.format(str(esx_list).strip('[]'))

            cursor.execute(sql_2)

            results_2 = cursor.fetchall()

            list_result_2 = __convert_db_results(cursor, results_2)

            for item in list_result_2:
                if item['CHILD_TIER_3'] == 'Application Instance':
                    if item['CHILD_DNSDOMAIN']:
                        vcenter_info_dict[item['PARENT_NAME']] = item['CHILD_NAME'] + '.' + item['CHILD_DNSDOMAIN'].upper()
                    else:
                        vcenter_info_dict[item['PARENT_NAME']] = item['CHILD_NAME']
                elif item['CHILD_TIER_3'] == 'Vmware ESX Server':
                    if item['PARENT_NAME'] not in cluster_info_dict.keys():
                        cluster_info_dict[item['PARENT_NAME']] = []
                    cluster_info_dict[item['PARENT_NAME']].append(item['CHILD_NAME'])
                else:
                    continue

        for device_info in list_result:
            if 'VMH' in device_info['CI_NAME']:
                if cluster_info_dict:
                    for cluster, esx in cluster_info_dict.items():
                        if device_info['CI_NAME'] in esx and cluster in vcenter_info_dict.keys():
                            device_info['VCENTER'] = vcenter_info_dict[cluster]
                        else:
                            device_info['VCENTER'] = ''
                else:
                    device_info['VCENTER'] = ''
            else:
                device_info['VCENTER'] = ''

        return list_result

    except Exception as e:
        logger.error('Error getting server deivce list: ' + str(e))
    finally:
        # Close the cursor
        cursor.close()
        # API requests statistics
        APIVisitStatistics.save_api_requests('CMDB', 'rb0orarac34.de.bosch.com', len(data_center_room_list) * 2)


def __get_network_device_list_from_db(connection, data_center_room_list):
    # Create cursor
    cursor = connection.cursor()

    try:
        sql = """select

                    name as ci_name
                    ,type_name as ci_type
                    ,status_reason
                    ,tier_2
                    ,tier_3
                    ,primary_support_group
                    ,datacenterroom as dcr

                    from
                        cmswhs.v_spl_h_item

                    where
                    datacenterroom in ({})

                    and status = 'Deployed'
                    and status_reason = 'Productive'
                    and tier_1 = 'Infrastructure'
                    and tier_2 = 'Network'

                    and primary_support_group in ('Network Datacenter Services')
        """.format(str(data_center_room_list).strip('[]'))

        cursor.execute(sql)

        results = cursor.fetchall()

        list_result = __convert_db_results(cursor, results)

        for device_item in list_result:
            device_item['ILO_IP'] = ''
            device_item['VCENTER'] = ''

        return list_result

    except Exception as e:
        logger.error('Error getting storage device list: ' + str(e))
    finally:
        # Close the cursor
        cursor.close()
        # API requests statistics
        APIVisitStatistics.save_api_requests('CMDB', 'rb0orarac34.de.bosch.com', len(data_center_room_list))



def get_data_from_db(host_list, select_attributes_dict):

    # Define return list
    reorganized_data_list = []
    # Connect to CMDB Oracle DB
    connection = oracledb.connect(user="CMS_SRE_R", password="Cw0soqxg!az20$re", dsn="rb0orarac34.de.bosch.com/ITCW_rb0orarac34.de.bosch.com", port="38000")

    try:
        # Create cursor
        cursor = connection.cursor()
        # Stitching sql sentence
        sql = __sql_stitching(host_list, select_attributes_dict)
        # Execute selection for the customized sql
        cursor.execute(sql)
        # Fetching all the selected data
        db_data = cursor.fetchall()

        # API requests statistics
        APIVisitStatistics.save_api_requests('CMDB', 'rb0orarac34.de.bosch.com', len(host_list))

        db_data_with_head = []
        select_head = []
        if db_data:
            for key, value in select_attributes_dict.items():
                if value:
                    select_head.append(key)

            for item in db_data:
                db_data_with_head.append(dict(zip(select_head, item)))

            reorganized_data_with_people = {}

            for data in db_data_with_head:
                reorganized_data_with_people_key = data['name'] + '_' + data['tier_2']
                if reorganized_data_with_people_key in reorganized_data_with_people.keys():
                    reorganized_data_with_people[reorganized_data_with_people_key]['used_by'] += (';' + data['used_by'])
                else:
                    reorganized_data_with_people[reorganized_data_with_people_key] = data

            reorganized_data_list = list(reorganized_data_with_people.values())
        else:
            return reorganized_data_list
    except Exception as e:
        logger.error('Error when execute Oracle DB search: ' + str(e))
    finally:
        # Close the DB connection
        connection.close()

    return reorganized_data_list


def get_pmc_device_list(data_center_room):
    storage_device_list = []
    server_device_list = []
    connection = oracledb.connect(user="CMS_SRE_R", password="Cw0soqxg!az20$re",
                                  dsn="rb0orarac34.de.bosch.com/ITCW_rb0orarac34.de.bosch.com", port="38000")
    try:
        data_center_room_list = data_center_room.split(';')
        logger.info('Retrieving device list for: ' + str(data_center_room_list))

        storage_device_list = __get_storage_device_list_from_db(connection, data_center_room_list)
        server_device_list = __get_server_device_list_from_db(connection, data_center_room_list)
        network_device_list = __get_network_device_list_from_db(connection, data_center_room_list)
    except Exception as e:
        logger.error('Error getting PMC device list: ' + str(e))
    finally:
        connection.close()

    return storage_device_list + server_device_list + network_device_list


def get_dcr_loc_contact(db_data_all):
    # Connect to CMDB Oracle DB
    connection = oracledb.connect(user="CMS_SRE_R", password="Cw0soqxg!az20$re",
                                  dsn="rb0orarac34.de.bosch.com/ITCW_rb0orarac34.de.bosch.com", port=38000)

    # Create cursor
    cursor = connection.cursor()
    try:
        dcr_list = []
        for db_data in db_data_all:
            dcr_list.append(db_data['DCR'])

        print(dcr_list)
        # Stitching sql sentence
        sql = """select

                a.name as ci_name
                ,b.corporate_id

                from
                    cmswhs.v_spl_h_item a

                    left outer JOIN cmswhs.v_spl_v_rel_i2i     s ON a.itcw_ref_id = s.itcw_ref_id_child
                    left outer JOIN cmswhs.v_spl_h_item       a2 ON s.itcw_ref_id_parent = a2.itcw_ref_id

                    inner join cmswhs.v_spl_v_rel_acc b on a2.itcw_ref_id = b.itcw_ref_id 

                where
                a.name in ({})
                and a2.tier_3 = 'LIS Location'
                and b.role_description = 'LIS Local Contact Onsite'

        """.format(str(dcr_list).upper().strip('[]'))

        # Execute selection for the customized sql
        cursor.execute(sql)
        # Fetching all the selected data
        db_data = cursor.fetchall()

        converted_db_data = __convert_db_results(cursor, db_data)

        print(converted_db_data)

        loc_data = {}

        for db_data in converted_db_data:
            loc_data[db_data['CI_NAME']] = db_data['CORPORATE_ID']

        for db_data in db_data_all:
            db_data['LOC_CONTACT'] = loc_data[db_data['DCR']]
        
        return db_data_all
        
    except Exception as e:
        print('Error querying Oracle DB: ' + str(e))
    finally:
        # Close the cursor
        cursor.close()
        # Close the connection
        connection.close()
        # API requests statistics


def get_hardware_info_from_db(host_list):

    # Connect to CMDB Oracle DB
    connection = oracledb.connect(user="CMS_SRE_R", password="Cw0soqxg!az20$re",
                                  dsn="rb0orarac34.de.bosch.com/ITCW_rb0orarac34.de.bosch.com", port=38000)

    # Create cursor
    cursor = connection.cursor()

    try:
        # Stitching sql sentence
        sql = """select

                a.name as ci_name
                ,a.type_name as ci_type
                ,a.status
                ,a.status_reason
                ,a.baselineci
                ,a.serial_number
                ,a.datacenterroom as dcr
                ,a.warrantydate
                ,a2.name as parent_ci
                ,a2.tier_3 as parent_type
                ,a2.fsx_contact
                ,a2.fsx_contact_email

                from
                    cmswhs.v_spl_h_item a

                    left outer JOIN cmswhs.v_spl_v_rel_i2i     s ON a.itcw_ref_id = s.itcw_ref_id_child
                    left outer JOIN cmswhs.v_spl_h_item       a2 ON s.itcw_ref_id_parent = a2.itcw_ref_id

                where
                a.name in ({})
                and (a.tier_1 = 'Server' or a.tier_1 = 'Infrastructure')
                and (a.tier_2 = 'Hardware' or a.tier_2 = 'Storage')
                and (a.tier_3 = 'X86 certified Hardware' or a.tier_3 = 'Disk Subsystem SAN' or a.tier_3 = 'NAS Storage System')
                and (a2.tier_3 = 'IP Address' or a2.tier_3 = 'Data Center Room')

        """.format(str(host_list).upper().strip('[]'))

        # Execute selection for the customized sql
        cursor.execute(sql)
        # Fetching all the selected data
        db_data = cursor.fetchall()

        converted_db_data = __convert_db_results(cursor, db_data)

        db_data_dict = {}
        for data in converted_db_data:
            if data['CI_NAME'] not in db_data_dict.keys():
                db_data_dict[data['CI_NAME']] = data
            if data['PARENT_TYPE'] == 'IP Address':
                if 'ILO_IP' not in db_data_dict[data['CI_NAME']].keys():
                    db_data_dict[data['CI_NAME']]['ILO_IP'] = data['PARENT_CI']
                else:
                    db_data_dict[data['CI_NAME']]['ILO_IP'] += (', ' + data['PARENT_CI'])
            else:
                db_data_dict[data['CI_NAME']]['FSX_CONTACT'] = data['FSX_CONTACT']
                db_data_dict[data['CI_NAME']]['FSX_CONTACT_EMAIL'] = data['FSX_CONTACT_EMAIL']
                db_data_dict[data['CI_NAME']]['WARRANTYDATE'] = str(data['WARRANTYDATE'])

        for hardware_info in db_data_dict.values():
            hardware_info.pop('PARENT_CI')
            hardware_info.pop('PARENT_TYPE')

        db_data_all = list(db_data_dict.values())

        return get_dcr_loc_contact(db_data_all)
    except Exception as e:
        logger.error('Error querying Oracle DB: ' + str(e))
    finally:
        # Close the cursor
        cursor.close()
        # Close the connection
        connection.close()
        # API requests statistics
        APIVisitStatistics.save_api_requests('CMDB', 'rb0orarac34.de.bosch.com', len(host_list))
