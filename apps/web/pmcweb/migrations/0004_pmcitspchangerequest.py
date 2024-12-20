# Generated by Django 3.2.15 on 2024-11-21 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pmcweb', '0003_pmcactivities_san_assignee'),
    ]

    operations = [
        migrations.CreateModel(
            name='PMCitspchangerequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('itsp_no', models.CharField(blank=True, max_length=100, null=True, verbose_name='ITSP No')),
                ('data_center_room', models.CharField(max_length=100, verbose_name='Data center room')),
                ('change_class', models.IntegerField(default=0, verbose_name='Change class')),
                ('reason', models.CharField(max_length=500, verbose_name='Reason')),
                ('start_date', models.CharField(max_length=20, verbose_name='Start date')),
                ('start_time', models.CharField(max_length=20, verbose_name='Start time')),
                ('end_date', models.CharField(max_length=20, verbose_name='End date')),
                ('end_time', models.CharField(max_length=20, verbose_name='End time')),
                ('start_with_shutdown', models.CharField(max_length=20, verbose_name='Start with shutdown')),
                ('region', models.CharField(max_length=20, verbose_name='Region')),
                ('location_code', models.CharField(max_length=20, verbose_name='Location code')),
                ('additional_people', models.CharField(blank=True, max_length=200, null=True, verbose_name='Additional people')),
                ('people_onsite', models.CharField(max_length=200, verbose_name='People onsite')),
                ('email_address', models.CharField(max_length=200, verbose_name='Email address')),
                ('contact_information', models.CharField(max_length=200, verbose_name='Contact information')),
                ('high_availability', models.IntegerField(default=0, verbose_name='High availability')),
                ('ha_server_oom', models.CharField(blank=True, max_length=200, null=True, verbose_name='Server room to failover')),
                ('ha_service', models.CharField(blank=True, max_length=200, null=True, verbose_name='service to failover')),
                ('pmc_start_time', models.IntegerField(verbose_name='PMC start time')),
                ('pmc_end_time', models.IntegerField(verbose_name='PMC end time')),
            ],
            options={
                'verbose_name': 'PMC ITSP Change Request',
                'verbose_name_plural': 'PMC ITSP Change Request',
                'db_table': 'pmc_itsp_change_request',
                'managed': True,
            },
        ),
    ]
