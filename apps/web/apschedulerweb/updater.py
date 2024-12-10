from apscheduler.schedulers.background import BackgroundScheduler
from apschedulerweb.cmdb_data_update import cmdb_data_update
from apschedulerweb.host_info_statistic import host_info_statistic


def start():
    scheduler = BackgroundScheduler()
    # Job No.1: Update CMDB data every 6 hours.
    # scheduler.add_job(cmdb_data_update, 'interval', hours=3)
    # Job No.2: Statistic hosts info every 24 hours.
    # scheduler.add_job(host_info_statistic, 'interval', hours=24)
    # scheduler.start()
