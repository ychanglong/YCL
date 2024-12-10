from django.db import models
from resource_base.modules.basetools import md5
import time

# User login account
# loginid, loginpwd, name, status, department, email, last_login, create_time, edit_time
class Account(models.Model):
    loginid = models.CharField(verbose_name="Login ID", max_length=20, primary_key=True, null=False, blank=False)
    loginpwd = models.CharField(verbose_name="Login Password", max_length=200, null=False, blank=False)
    name = models.CharField(verbose_name="Name", max_length=50, null=False, blank=False)
    status = models.BooleanField(verbose_name="Status", null=False, blank=False, default=0)
    admin = models.BooleanField(verbose_name="Admin", null=False, blank=False, default=0)
    pmc_coordinator = models.BooleanField(verbose_name="PMC coordinator", null=False, blank=False, default=0)
    pmc_operator = models.BooleanField(verbose_name="PMC operator", null=False, blank=False, default=0)
    guest_account = models.BooleanField(verbose_name="Guest account", null=False, blank=False, default=0)
    department = models.CharField(verbose_name="Department", max_length=50, blank=True, null=True, default=None)
    location = models.CharField(verbose_name="Location", max_length=100, blank=True, null=True, default=None)
    email = models.CharField(verbose_name="Email address", max_length=100, null=True, blank=True, default=None)
    avatar = models.ImageField(verbose_name="Avatar", upload_to='avatar', null=True, default="empty.empty")
    last_login = models.IntegerField(verbose_name="Last login", null=True, blank=True, default=None)
    create_time = models.IntegerField(verbose_name="Create time", null=True, blank=True, default=int(time.time()))
    edit_time = models.IntegerField(verbose_name="Modify time", null=True, blank=True, default=None)

    class Meta:
        managed = True
        app_label = 'userweb'
        db_table = "user_account"
        verbose_name = "User Accounts"
        verbose_name_plural = "User Accounts"

    def __str__(self):
        return "%s" % self.name

