from django.db import models
from django.core.cache import caches
import time
import logging

# Get the django logger
logger = logging.getLogger('django')

# API visit statistics
# service_name, api_url, request_amount, request_time
class APIVisitStatistics(models.Model):
    service_name = models.CharField(verbose_name="Service name", max_length=100, null=False, blank=False)
    api_url = models.CharField(verbose_name="API url", max_length=200, null=False, blank=False)
    request_amount = models.IntegerField(verbose_name="Request amount", null=False, blank=False)
    request_time = models.IntegerField(verbose_name="Request time", default=int(time.time()))

    class Meta:
        managed = True
        app_label = 'mainweb'
        db_table = "api_visit_statistics"
        verbose_name = "API Visit Statistics"
        verbose_name_plural = "API Visit Statistics"

    @classmethod
    def save_api_requests(cls, service_name, api_url, request_amount):

        return cls.objects.create(
            service_name=service_name,
            api_url=api_url,
            request_amount=request_amount,
            request_time=int(time.time()),
        )

    def __str__(self):
        return "%s" % self.api_url


# URL visit statistics
# service_name, api_url, request_amount, request_time
class AppVisitStatistics(models.Model):
    app_name = models.CharField(verbose_name="Service name", max_length=100, null=False, blank=False)
    app_url = models.CharField(verbose_name="API url", max_length=200, null=False, blank=False)
    request_amount = models.IntegerField(verbose_name="Request amount", null=False, blank=False)
    statistic_time = models.IntegerField(verbose_name="Statistic time", default=int(time.time()))

    class Meta:
        managed = True
        app_label = 'mainweb'
        db_table = "app_visit_statistics"
        verbose_name = "App Visit Statistics"
        verbose_name_plural = "App Visit Statistics"

    @classmethod
    def save_app_requests(cls, app_name, app_url):
        cache = caches['default']

        try:
            if cache.get(app_url):
                cache.incr(app_url, delta=1)
                if cache.get(app_url) == 99:
                    cls.objects.create(
                        app_name=app_name,
                        app_url=app_url,
                        request_amount=99,
                        statistic_time=int(time.time()),
                    )
            else:
                cache.set(app_url, 1, timeout=24*60*60*7)

        except Exception as e:
            logger.error('Error saving app requests statistics data: %s' % (str(e),))
            return False

    def __str__(self):
        return "%s" % self.api_url


# Number of hosts statistics
# os_type, quantity, statistic_time
class HostsStatistics(models.Model):
    os_type = models.CharField(verbose_name="OS type", max_length=100, null=False, blank=False)
    quantity = models.IntegerField(verbose_name="Host quantity", null=False, blank=False)
    statistic_time = models.IntegerField(verbose_name="Statistic time", default=int(time.time()))

    class Meta:
        managed = True
        app_label = 'mainweb'
        db_table = "hosts_statistics"
        verbose_name = "Hosts Statistics"
        verbose_name_plural = "Hosts Statistics"

    def __str__(self):
        return "%s" % self.os_type


# Time saving statistics
# app_name, time_saved, request_time
class TimeSavingStatistics(models.Model):
    app_name = models.CharField(verbose_name="Service name", max_length=100, null=False, blank=False)
    # Seconds
    time_saved = models.IntegerField(verbose_name="Time saved", null=False, blank=False)
    request_time = models.IntegerField(verbose_name="Request time", default=int(time.time()))

    class Meta:
        managed = True
        app_label = 'mainweb'
        db_table = "time_saving_statistics"
        verbose_name = "Time Saving Statistics"
        verbose_name_plural = "Time Saving Statistics"

    @classmethod
    def time_saving_statistic(cls, app_name, time_saved):
        try:
            cls.objects.create(
                app_name=app_name,
                time_saved=time_saved,
                request_time=int(time.time())
            )

        except Exception as e:
            logger.error('Error saving time saving statistics data: %s' % (str(e),))
            return False

    def __str__(self):
        return "%s" % self.app_name