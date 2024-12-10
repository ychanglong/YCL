from django.db import models

# Host Info
# Host name, OS type, Status
class HostInfo(models.Model):
    host_id = models.AutoField(verbose_name="Host ID", primary_key=True)
    host_name = models.CharField(verbose_name="Host Name", max_length=100, null=True, blank=True)
    dns_domain = models.CharField(verbose_name="DNS Domain", max_length=100, null=True, blank=True)
    status = models.CharField(verbose_name="Status", max_length=100, null=True, blank=True)
    status_reason = models.CharField(verbose_name="Status Reason", max_length=100, null=True, blank=True)
    os_type = models.CharField(verbose_name="OS Type", max_length=100, null=True, blank=True)
    used_by = models.CharField(verbose_name="Used By", max_length=100, null=True, blank=True)

    class Meta:
        managed = True
        app_label = 'monitoringweb'
        db_table = "host_info"
        verbose_name = "Host Information"
        verbose_name_plural = "Host Information"

    def __str__(self):
        return "%s" % self.host_name
