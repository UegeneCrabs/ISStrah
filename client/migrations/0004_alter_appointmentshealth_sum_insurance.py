# Generated by Django 4.2.6 on 2024-02-20 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0003_paymenttablehealth_contracthealth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentshealth',
            name='sum_insurance',
            field=models.IntegerField(choices=[(1.1, 100000), (1.3, 250000), (1.5, 500000)], verbose_name='Сумма страхования'),
        ),
    ]