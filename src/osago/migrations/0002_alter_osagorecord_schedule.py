# Generated by Django 4.2.6 on 2024-05-14 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_agentschedule_options_and_more'),
        ('osago', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='osagorecord',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.agentschedule', verbose_name='Расписание агента'),
        ),
    ]
