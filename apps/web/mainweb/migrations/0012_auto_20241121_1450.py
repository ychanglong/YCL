# Generated by Django 3.2.15 on 2024-11-21 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainweb', '0011_auto_20241117_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apivisitstatistics',
            name='request_time',
            field=models.IntegerField(default=1732171813, verbose_name='Request time'),
        ),
        migrations.AlterField(
            model_name='appvisitstatistics',
            name='statistic_time',
            field=models.IntegerField(default=1732171813, verbose_name='Statistic time'),
        ),
        migrations.AlterField(
            model_name='hostsstatistics',
            name='statistic_time',
            field=models.IntegerField(default=1732171813, verbose_name='Statistic time'),
        ),
        migrations.AlterField(
            model_name='timesavingstatistics',
            name='request_time',
            field=models.IntegerField(default=1732171813, verbose_name='Request time'),
        ),
    ]
