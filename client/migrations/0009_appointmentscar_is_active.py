# Generated by Django 4.2.6 on 2024-02-25 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0008_alter_appointmentshealth_age_coefficient_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointmentscar',
            name='is_active',
            field=models.BooleanField(default=False, null=True, verbose_name='Проработана'),
        ),
    ]