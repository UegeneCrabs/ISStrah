# Generated by Django 4.2.6 on 2024-05-16 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('life', '0005_remove_healthclaim_appraiser_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lifeinsurancerecord',
            name='competition_participation',
            field=models.BooleanField(blank=True, null=True, verbose_name='Участие в соревнованиях'),
        ),
    ]
