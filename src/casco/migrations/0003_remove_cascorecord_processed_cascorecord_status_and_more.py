# Generated by Django 4.2.6 on 2024-05-14 03:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_agentschedule_options_and_more'),
        ('casco', '0002_carmodel_coefficient'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cascorecord',
            name='processed',
        ),
        migrations.AddField(
            model_name='cascorecord',
            name='status',
            field=models.CharField(choices=[('pending', 'Ожидает'), ('in_progress', 'В работе'), ('completed', 'Завершена')], default='pending', max_length=20, verbose_name='Статус'),
        ),
        migrations.AlterField(
            model_name='cascorecord',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.agentschedule', verbose_name='Расписание агента'),
        ),
    ]