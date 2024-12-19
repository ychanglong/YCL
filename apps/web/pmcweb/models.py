from django.db import models


# PMC Activities
# pmc_id, itsp_no, data_center_room, change_class, reason, start_time, end_time, start_with_shutdown, region, location_code, additional_people, people_onsite, engineer_address
# contact_information, change_number, status, power_off_assignee, power_on_assignee, san, nas, backup, oracle_db
class PMCActivities(models.Model):
    pmc_id = models.AutoField(verbose_name="PMC ID", primary_key=True)
    # data_status: 0: Inactive, 1: Active
    data_status = models.IntegerField(verbose_name="Data status", default=1, null=False, blank=False)
    itsp_no = models.CharField(verbose_name="ITSP No", max_length=100, null=True, blank=True)
    data_center_room = models.CharField(verbose_name="Data center room", max_length=100, null=False, blank=False)
    # change_class: 0: class 0, 1: class 1, 2: class 2, 3: Emergency, 4: To be checked
    change_class = models.IntegerField(verbose_name="Change class", null=False, blank=False, default=0)
    reason = models.CharField(verbose_name="Reason", max_length=500, blank=False, null=False)
    start_time = models.IntegerField(verbose_name="Start time", blank=False, null=False)
    end_time = models.IntegerField(verbose_name="End time", null=False, blank=False)
    start_with_shutdown = models.CharField(verbose_name="Start with shutdown", max_length=20, null=False, blank=False)
    region = models.CharField(verbose_name="Region", max_length=20, null=False, blank=False)
    location_code = models.CharField(verbose_name="Location code", max_length=20, null=False, blank=False)
    additional_people = models.CharField(verbose_name="Additional people", max_length=200, null=True, blank=True)
    people_onsite = models.CharField(verbose_name="People onsite", max_length=200, null=False, blank=False)
    engineer_address = models.CharField(verbose_name="Engineer address", max_length=200, null=False, blank=False)
    contact_information = models.CharField(verbose_name="Contact information", max_length=200, null=False, blank=False)
    change_number = models.CharField(verbose_name="Change number", max_length=40, null=False, blank=False)
    # status: 0: New, 1: In progress, 2: Pending, 3: Scheduled, 4: Completed, 5: Cancelled
    status = models.IntegerField(verbose_name="Status", null=False, blank=False)
    power_off_assignee = models.CharField(verbose_name="Power off assignee", max_length=100, null=True, blank=True)
    power_on_assignee = models.CharField(verbose_name="Power on assignee", max_length=100, null=True, blank=True)
    # san_VNX: 0: No, 1: Yes, 2: To be checked
    san_vnx = models.IntegerField(verbose_name="SAN VNX", default=0, null=False, blank=False)
    # san_Unity: 0: No, 1: Yes, 2: To be checked
    san_unity = models.IntegerField(verbose_name="SAN Unity", default=0, null=False, blank=False)
    # san_VPLEX: 0: No, 1: Yes, 2: To be checked
    san_vplex = models.IntegerField(verbose_name="SAN VPLEX", default=0, null=False, blank=False)
    # nas: 0: No, 1: Yes, 2: To be checked
    nas = models.IntegerField(verbose_name="NAS", default=0, null=False, blank=False)
    # backup: 0: No, 1: Yes, 2: To be checked
    backup = models.IntegerField(verbose_name="Backup", default=0, null=False, blank=False)
    # oracle_db: 0: No, 1: Yes, 2: To be checked
    oracle_db = models.IntegerField(verbose_name="Oracle DB", default=0, null=False, blank=False)
    # Identify if the notification Email was sent： 0： No, 1: Yes
    email_notification = models.IntegerField(verbose_name="Email Notification", default=0, null=False, blank=False)
    # High availability: 0: No, 1: Yes
    high_availability = models.IntegerField(verbose_name="High availability", default=0, null=False, blank=False)
    # Server room to failover
    server_room_to_failover = models.CharField(verbose_name="Server room to failover", max_length=200, null=True, blank=True)
    # Service to failover
    service_to_failover = models.CharField(verbose_name="service to failover", max_length=200, null=True, blank=True)
    # Backup assignee (When backup is YES)
    backup_assignee = models.CharField(verbose_name="Backup assignee", max_length=100, null=True, blank=True)
    # oracle_db_assignee (When oracle_db is YES)
    oracle_db_assignee = models.CharField(verbose_name="Oracle DB assignee", max_length=100, null=True, blank=True)
    # PMC coordinator
    pmc_coordinator = models.CharField(verbose_name="PMC coordinator", max_length=100, null=True, blank=True)
    # SAN assignee
    san_assignee = models.CharField(verbose_name="SAN assignee", max_length=100, null=True, blank=True)

    @classmethod
    def save_pmc_activity(cls, pmc_activity):
        return cls.objects.create(
            itsp_no=pmc_activity.itsp_no,
            data_center_room=pmc_activity.data_center_room,
            change_class=pmc_activity.change_class,
            reason=pmc_activity.reason,
            start_time=pmc_activity.start_time,
            end_time=pmc_activity.end_time,
            start_with_shutdown=pmc_activity.start_with_shutdown,
            region=pmc_activity.region,
            location_code=pmc_activity.location_code,
            additional_people=pmc_activity.additional_people,
            people_onsite=pmc_activity.people_onsite,
            engineer_address=pmc_activity.engineer_address,
            contact_information=pmc_activity.contact_information,
            change_number=pmc_activity.change_number,
            status=pmc_activity.status,
            power_off_assignee=pmc_activity.power_off_assignee,
            power_on_assignee=pmc_activity.power_on_assignee,
            san_vnx=pmc_activity.san_vnx,
            san_unity=pmc_activity.san_unity,
            san_vplex=pmc_activity.san_vplex,
            nas=pmc_activity.nas,
            backup=pmc_activity.backup,
            oracle_db=pmc_activity.oracle_db,
            high_availability = pmc_activity.high_availability,
            server_room_to_failover = pmc_activity.server_room_to_failover,
            service_to_failover = pmc_activity.service_to_failover,
            backup_assignee = pmc_activity.backup_assignee,
            oracle_db_assignee = pmc_activity.oracle_db_assignee,
            pmc_coordinator = pmc_activity.pmc_coordinator,
            san_assignee = pmc_activity.san_assignee
        )

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_activities"
        verbose_name = "PMC Activities"
        verbose_name_plural = "PMC Activities"

    def __str__(self):
        return "%s" % self.pmc_id


# PMC Assignee
# assignee_id, assignee_nt, assignee_name, assignee_department, assignee_email, assignee_responsible
class PMCAssignee(models.Model):
    assignee_id = models.IntegerField(verbose_name="Assignee ID", primary_key=True)
    assignee_nt = models.CharField(verbose_name="Assignee NT account", max_length=20, null=False, blank=False)
    assignee_name = models.CharField(verbose_name="Assignee Name", max_length=100, null=False, blank=False)
    assignee_department = models.CharField(verbose_name="Assignee Department", max_length=100, null=False, blank=False)
    assignee_email = models.CharField(verbose_name="Assignee Email", max_length=100, null=False, blank=False)
    assignee_responsible = models.CharField(verbose_name="Assignee Responsible", max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_assignee"
        verbose_name = "PMC Assignee"
        verbose_name_plural = "PMC Assignee"

    def __str__(self):
        return "%s" % self.assignee_nt


# PMC Operation
class PMCOperation(models.Model):
    pmc_id = models.IntegerField(verbose_name="PMC ID", default=0, null=False, blank=False)
    pmc_confirmed = models.IntegerField(verbose_name="PMC Confrimed", default=0, null=False, blank=False)
    device_name = models.CharField(verbose_name="Device Name", max_length=100, null=False, blank=False)
    ilo_ip = models.CharField(verbose_name="ILO IP", max_length=100, null=True, blank=True)
    vcenter_fqdn = models.CharField(verbose_name="vCenter FQDN", max_length=100, null=True, blank=True)
    esx_flag = models.IntegerField(verbose_name="ESX Flag", default=0, null=False, blank=False)
    nas_cluster_flag = models.IntegerField(verbose_name="NAS Cluster Flag", default=0, null=False, blank=False)

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_operation"
        verbose_name = "PMC Operation"
        verbose_name_plural = "PMC Operation"

    def __str__(self):
        return "%s" % self.pmc_id


# PMC Device list
class PMCDevicelist(models.Model):
    pmc_id = models.IntegerField(verbose_name="PMC ID", default=0, null=False, blank=False)
    device_name = models.CharField(verbose_name="Device Name", max_length=100, null=False, blank=False)
    ilo_ip = models.CharField(verbose_name="ILO IP", max_length=100, null=True, blank=True)
    vcenter = models.CharField(verbose_name="vCenter", max_length=100, null=True, blank=True)
    data_center_room = models.CharField(verbose_name="DCR", max_length=100, null=True, blank=True)
    ci_type = models.CharField(verbose_name="CI Type", max_length=100, null=True, blank=True)
    tier_2 = models.CharField(verbose_name="Tier 2", max_length=100, null=True, blank=True)
    tier_3 = models.CharField(verbose_name="Tier 3", max_length=100, null=True, blank=True)
    status = models.CharField(verbose_name="Status", max_length=100, null=True, blank=True)
    support_group = models.CharField(verbose_name="Support group", max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_device_list"
        verbose_name = "PMC Device List"
        verbose_name_plural = "PMC Device List"

    def __str__(self):
        return "%s" % self.pmc_id


# PMC Activity plan
class PMCActivityplan(models.Model):
    pmc_id = models.IntegerField(verbose_name="PMC ID", default=0, null=False, blank=False)
    line_number = models.IntegerField(verbose_name="Line number", default=0, null=False, blank=False)
    date_start = models.CharField(verbose_name="Date start", max_length=100, blank=True, null=True)
    start_time = models.CharField(verbose_name="Start time", max_length=100, blank=True, null=True)
    description_of_activity = models.CharField(verbose_name="Description of activity", max_length=500, blank=True, null=True)
    execution = models.CharField(verbose_name="Execution", max_length=500, blank=True, null=True)
    responsible = models.CharField(verbose_name="Responsible", max_length=500, blank=True, null=True)
    information_to = models.CharField(verbose_name="Start time", max_length=500, blank=True, null=True)

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_activity_plan"
        verbose_name = "PMC Activity Plan"
        verbose_name_plural = "PMC Activity Plan"

    def __str__(self):
        return "%s" % self.pmc_id


# Backup schedule list
class PMCBackupschedule(models.Model):
    pmc_activity = models.ForeignKey(PMCActivities, on_delete=models.CASCADE, related_name='backup_schedule')
    schedule_id =  models.CharField(verbose_name="Schedule ID", max_length=40, null=True, blank=True)
    change_number = models.CharField(verbose_name="Change number", max_length=40, null=False, blank=False)
    backup_device_name = models.CharField(verbose_name="Device Name", max_length=100, null=False, blank=False)
    start_time = models.IntegerField(verbose_name="Start time", blank=False, null=False)
    end_time = models.IntegerField(verbose_name="End time", null=False, blank=False)
    # status: 0: Cancelled, 1: Scheduled, 2: Completed
    schedule_status = models.IntegerField(verbose_name="Schedule Status", default=1, null=False, blank=False)

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_backup_schedule"
        verbose_name = "PMC Backup Schedule"
        verbose_name_plural = "PMC Backup Schedule"

    def __str__(self):
        return "%s" % self.schedule_id


# PMC ITSP change reuqest data
class PMCitspchangerequest(models.Model):
    itsp_no = models.CharField(verbose_name="ITSP No", max_length=100, null=True, blank=True)
    data_center_room = models.CharField(verbose_name="Data center room", max_length=100, null=False, blank=False)
    # change_class: 0: class 0, 1: class 1, 2: class 2, 3: Emergency, 4: To be checked
    change_class = models.IntegerField(verbose_name="Change class", null=False, blank=False, default=0)
    reason = models.CharField(verbose_name="Reason", max_length=500, blank=False, null=False)
    start_date = models.CharField(verbose_name="Start date", max_length=20, null=False, blank=False)
    start_time = models.CharField(verbose_name="Start time", max_length=20, null=False, blank=False)
    end_date = models.CharField(verbose_name="End date", max_length=20, null=False, blank=False)
    end_time = models.CharField(verbose_name="End time", max_length=20, null=False, blank=False)
    start_with_shutdown = models.CharField(verbose_name="Start with shutdown", max_length=20, null=False, blank=False)
    region = models.CharField(verbose_name="Region", max_length=20, null=False, blank=False)
    location_code = models.CharField(verbose_name="Location code", max_length=20, null=False, blank=False)
    additional_people = models.CharField(verbose_name="Additional people", max_length=200, null=True, blank=True)
    people_onsite = models.CharField(verbose_name="People onsite", max_length=200, null=False, blank=False)
    email_address = models.CharField(verbose_name="Email address", max_length=200, null=False, blank=False)
    contact_information = models.CharField(verbose_name="Contact information", max_length=200, null=False, blank=False)
    # High availability: 0: No, 1: Yes
    high_availability = models.IntegerField(verbose_name="High availability", default=0, null=False, blank=False)
    # Server room to failover
    ha_server_oom = models.CharField(verbose_name="Server room to failover", max_length=200, null=True, blank=True)
    # Service to failover
    ha_service = models.CharField(verbose_name="service to failover", max_length=200, null=True, blank=True)
    pmc_start_time = models.IntegerField(verbose_name="PMC start time", blank=False, null=False)
    pmc_end_time = models.IntegerField(verbose_name="PMC end time", blank=False, null=False)

    class Meta:
        managed = True
        app_label = 'pmcweb'
        db_table = "pmc_itsp_change_request"
        verbose_name = "PMC ITSP Change Request"
        verbose_name_plural = "PMC ITSP Change Request"

    def __str__(self):
        return "%s" % self.itsp_no