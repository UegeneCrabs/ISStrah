# Generated by Django 4.2.6 on 2024-05-15 21:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('casco', '0007_remove_driverscascorecord_casco_record_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cascoclaim',
            name='processed',
        ),
        migrations.AddField(
            model_name='cascoclaim',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Ожидает'), ('in_progress', 'В работе'), ('completed', 'Завершена')], default='pending', max_length=20, null=True, verbose_name='Статус'),
        ),
    ]
