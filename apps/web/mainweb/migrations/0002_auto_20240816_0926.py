# Generated by Django 3.2.15 on 2024-08-16 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mainweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='apivisitstatistics',
            name='request_time',
            field=models.IntegerField(default=1723771566, verbose_name='Request time'),
        ),
        migrations.AlterField(
            model_name='appvisitstatistics',
            name='statistic_time',
            field=models.IntegerField(default=1723771566, verbose_name='Statistic time'),
        ),
        migrations.AlterField(
            model_name='hostsstatistics',
            name='statistic_time',
            field=models.IntegerField(default=1723771566, verbose_name='Statistic time'),
        ),
        migrations.AlterField(
            model_name='timesavingstatistics',
            name='request_time',
            field=models.IntegerField(default=1723771566, verbose_name='Request time'),
        ),
    ]