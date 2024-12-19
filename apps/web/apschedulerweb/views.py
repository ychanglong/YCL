# -*- coding: utf-8 -*-
# @Time        : 2023/07/27
# @Author      : MA Jared (BD/PIO3)
# @Bitbucket   : https://sourcecode.socialcoding.bosch.com/users/maa9szh/repos/goc_automation/browse
# @Application : Apscheduler
# @Project     : GOC Automation Platform

import logging
import oracledb
import time
import importlib
from django.conf import settings
from django.core import mail
from resource_base.modules.importModules import *
from django.db.backends.utils import CursorWrapper
from django.core.cache import caches
from monitoringweb.models import HostInfo
from mainweb.models import HostsStatistics
from pmcweb.models import PMCActivities
from userweb.models import Account
from operationweb.scripts import email_factory
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(), "default")

# Get the django logger
logger = logging.getLogger('django')

def ensure_mysql_connection():
    for name, config in settings.DATABASES.items():
        module = importlib.import_module(config["ENGINE"] + ".base")

        def ensure_connection(self):
            if self.connection is not None:
                try:
                    with CursorWrapper(self.create_cursor(), self) as cursor:
                        cursor.execute("SELECT 1")
                    return
                except Exception:
                    pass

            with self.wrap_database_errors:
                self.connect()

        module.DatabaseWrapper.ensure_connection = ensure_connection


def __acquire_lock(lock_name, expiration=60):
    """
    尝试获取锁，并在获取成功时返回True，否则返回False。
    """
    cache = caches['default']
    lock_key = f"lock:{lock_name}"
    # 使用Django缓存的add方法尝试获取锁
    acquired = cache.add(lock_key, "locked", expiration)
    return acquired


def __release_lock(lock_name):
    """
    释放锁。
    """
    cache = caches['default']
    lock_key = f"lock:{lock_name}"
    # 使用Django缓存的delete方法释放锁
    cache.delete(lock_key)


@register_job(scheduler, 'cron', hour=6, minute=30 , id='host_info_statistic', replace_existing=True)
def host_info_statistic():
    cache = caches['default']

    if __acquire_lock('host_info_statistic_lock', expiration=5):
        try:
            quantity_dict = {'windows_server': 0, 'unix_server': 0}
            c_host_list = cache.get_many(cache.keys("*_os_type"))

            for host in c_host_list.items():
                if host[1] == 'windows server':
                    quantity_dict['windows_server'] += 1
                elif host[1] == 'unix server':
                    quantity_dict['unix_server'] += 1
            logger.info('Windows server quantity: ' + str(quantity_dict['windows_server']))
            logger.info('Unix server quantity: ' + str(quantity_dict['unix_server']))

            # To fix (2013 'lost connection to mysql server during query')
            ensure_mysql_connection()

            for os_type, quantity in quantity_dict.items():
                HostsStatistics.objects.create(
                    os_type=os_type,
                    quantity=quantity,
                    statistic_time=int(time.time()),
                )
        except Exception as e:
            logger.error('Error saving hosts statistics data: %s' % (str(e),))
        finally:
            __release_lock('host_info_statistic_lock')


@register_job(scheduler, 'interval', hours=3, id='cmdb_data_update', replace_existing=True)
def cmdb_data_update():
    # Use CACHES default settings in settings.py
    cache = caches['default']

    if __acquire_lock('cmdb_data_update_lock', expiration=500):
        start_time = time.time()
        # To save CMDB data from Oracle DB
        cmdb_data_list = []

        # Get the CMDB data from Oracle DB
        connection = oracledb.connect(user="CMS_SRE_R", password="Cw0soqxg!az20$re",
                                    dsn="rb0orarac34.de.bosch.com/ITCW_rb0orarac34.de.bosch.com", port=38000)

        try:
            logger.info('Start to query CMDB data from Oracle DB.')
            oracle_start_time = time.time()

            cursor = connection.cursor()
            sql = """SELECT
                a.name
                ,a.dnsdomain
                ,a.status
                ,a.status_reason
                ,a.tier_3
                ,b.email_address
                ,b.role

                FROM cmswhs.v_spl_h_item a
                inner join cmswhs.v_spl_v_rel_acc b
                on a.itcw_ref_id = b.itcw_ref_id

                WHERE a.name IN (select a.name from cmswhs.v_spl_h_item a left outer join cmswhs.v_spl_v_rel_sg b on a.itcw_ref_id = b.itcw_ref_id where
                (a.primary_support_group = 'Server Operation Center'
                or b.SUPPORT_GROUP_NAME = 'Server Operation Center')
                and a.tier_2 = 'OS Instance'
                and a.status = 'Deployed')
                and a.tier_2 = 'OS Instance'
                and a.status = 'Deployed'
                and (b.role = 'Used by' or b.role = 'Managed by')"""

            cursor.execute(sql)
            cmdb_data_list = cursor.fetchall()

            logger.info("Oracle DB execute time: " + str(time.time() - oracle_start_time))

        except Exception as e:
            logger.error('Error querying Oracle DB: ' + str(e))
        finally:
            # Close the Oracle DB connection
            connection.close()

        # Update the CMDB data to MySQL DB
        try:
            logger.info('Start to insert CMDB data into MySQL DB.')

            if cmdb_data_list:
                # Delete all host info from MySQL
                delete_start_time = time.time()
                HostInfo.objects.all().delete()

                logger.info("MySQL deletion execute time: " + str(time.time() - delete_start_time))

                # Inert new host info into MySQL
                insert_start_time = time.time()
                host_info_insert = []
                for cmdb_data in cmdb_data_list:
                    if cmdb_data[6] == 'Used by':
                        host_info_insert.append(HostInfo(host_name=cmdb_data[0], dns_domain=cmdb_data[1], status=cmdb_data[2], status_reason=cmdb_data[3], os_type=cmdb_data[4], used_by=cmdb_data[5]))
                    else:
                        host_info_insert.append(HostInfo(host_name=cmdb_data[0], dns_domain=cmdb_data[1], status=cmdb_data[2], status_reason=cmdb_data[3], os_type=cmdb_data[4], used_by=''))
                HostInfo.objects.bulk_create(host_info_insert)

                logger.info("Mysql insert execute time: " + str(time.time() - insert_start_time))

            else:
                logger.warning('No CMDB data received from Oracle DB, skipping insert into MySQL.')

        except Exception as e:
            logger.error('Error writing into MySQL DB: ' + str(e))

        # Cache the CMDB data from MySQL to Redis
        try:

            logger.info('Start synchronizing MySQL CMDB data to Redis cache.')
            cache_start_time = time.time()

            # Query all the data from MySQL server_info table
            host_list = list(HostInfo.objects.all())

            # Save the server info to cache_data
            cache_data = {}

            optimized_host_data = {}
            for host in host_list:
                key_used_by = (host.host_name + '_used_by').lower()
                key_dns_domain = (host.host_name + '_dns_domain').lower()
                key_os_type = (host.host_name + '_os_type').lower()

                if key_used_by not in optimized_host_data.keys():
                    optimized_host_data[key_used_by] = ''
                else:
                    if host.used_by:
                        optimized_host_data[key_used_by] += (host.used_by + '; ')

                if host.dns_domain and (key_dns_domain not in optimized_host_data.keys()):
                    optimized_host_data[key_dns_domain] = host.dns_domain.lower()
                else:
                    continue

                if host.os_type and (key_os_type not in optimized_host_data.keys()):
                    optimized_host_data[key_os_type] = host.os_type.lower()
                else:
                    continue

            for key, value in optimized_host_data.items():
                if '_used_by' in key:
                    cache_data[key] = value[:-2]
                elif ('_dns_domain' in key) or ('_os_type' in key):
                    cache_data[key] = value
                else:
                    continue

            # Save host info to Redis, keep 7 days
            cache.set_many(cache_data, 24 * 60 * 60 * 7)

            logger.info('Redis data synchronization execute time: ' + str(time.time() - cache_start_time))
            logger.info("Total execute time: " + str(time.time() - start_time))

        except Exception as e:
            logger.error("Error caching CMDB data to Redis: " + str(e))
        finally:
            __release_lock('cmdb_data_update_lock')


# @register_job(scheduler, 'cron', hour=8, minute=30 , id='pmc_coordinator_notification', replace_existing=True)
# def pmc_coordinator_notification():

#     # Use CACHES default settings in settings.py
#     cache = caches['default']

#     if __acquire_lock('pmc_coordinator_notification_lock', expiration=20):
#         try:
#             # Get the date in time array format
#             three_days_ago = (datetime.datetime.now() - datetime.timedelta(days=int(3)))
#             # Convert to timestamp
#             time_stamp_three_days_ago = int(time.mktime(three_days_ago.timetuple()))

#             three_days_pmc_data = list(PMCActivities.objects.filter(Q(end_time__lte=time_stamp_three_days_ago) & Q(data_status=1)).exclude(status=4).exclude(status=5))

#             if three_days_pmc_data:

#                 pmc_coordinators = list(Account.objects.filter(pmc_coordinator=1))

#                 coordinator_emails = []

#                 for coordinator in pmc_coordinators:
#                     coordinator_emails.append(coordinator.email)

#                 # Set default from and cc Email address
#                 from_email = 'CI-Server-Operation-Center@cn.bosch.com'
#                 cc_email = ['CI-Server-Operation-Center@cn.bosch.com', 'jared.ma@cn.bosch.com']

#                 pmc_data_for_email_content = []
#                 for pmc_data in three_days_pmc_data:
#                     temp_data = [pmc_data.itsp_no, pmc_data.change_number, pmc_data.region, pmc_data.status, pmc_data.end_time]
#                     pmc_data_for_email_content.append(temp_data)

#                 logger.info('Three days exceeded PMC activity: ' + str(pmc_data_for_email_content))
#                 email_msg = {'subject': '[Reminder] PMC Activity status need to be update', 'content': email_factory.get_pmc_notification_msg(pmc_data_for_email_content)}

#                 # Initiate the Email message by EmailMessage
#                 msg = mail.EmailMessage(subject=email_msg['subject'], body=email_msg['content'],
#                                         from_email=from_email, to=coordinator_emails,
#                                         cc=cc_email)
#                 # Adjust the Email content type to html
#                 msg.content_subtype = 'html'
#                 delivered_mails = msg.send()

#                 logger.info('PMC coordinator notification Email successfully sent: ' + str(delivered_mails))
#             else:
#                 logger.info('No PMC activity exceed the end time, skip the notification Email sending.')
#         except Exception as e:
#             logger.error("Error sending PMC coordinator daily notification Email: " + str(e))
#         finally:
#             __release_lock('pmc_coordinator_notification_lock')

scheduler.start()
