# Generated by Django 4.2.6 on 2024-05-15 22:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('casco', '0009_remove_cascoclaim_insurance_appraiser_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='carmodel',
            name='coefficient',
        ),
    ]