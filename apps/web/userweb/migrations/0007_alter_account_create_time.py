# Generated by Django 3.2.15 on 2024-10-10 06:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userweb', '0006_alter_account_create_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='create_time',
            field=models.IntegerField(blank=True, default=1728543545, null=True, verbose_name='Create time'),
        ),
    ]