# Generated by Django 3.2.15 on 2024-08-16 01:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userweb', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='guest_account',
        ),
        migrations.AlterField(
            model_name='account',
            name='create_time',
            field=models.IntegerField(blank=True, default=1723771566, null=True, verbose_name='Create time'),
        ),
    ]
