# Generated by Django 4.2.6 on 2024-05-14 21:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casco', '0004_alter_cascorecord_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cascorecord',
            name='number_of_drivers',
        ),
        migrations.AddField(
            model_name='cascorecord',
            name='driver_restriction',
            field=models.CharField(choices=[('restricted', 'Ограниченный'), ('unrestricted', 'Неограниченный')], default='restricted', max_length=20, verbose_name='Ограничение водителей'),
        ),
    ]
