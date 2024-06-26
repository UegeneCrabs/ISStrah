# Generated by Django 4.2.6 on 2024-05-14 15:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0002_alter_lifepayoutassessment_damage_character'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lifeinsurancerecord',
            name='processed',
        ),
        migrations.AddField(
            model_name='lifeinsurancerecord',
            name='status',
            field=models.CharField(blank=True, choices=[('pending', 'Ожидает'), ('in_progress', 'В работе'), ('completed', 'Завершена')], default='pending', max_length=20, null=True, verbose_name='Статус'),
        ),
    ]
