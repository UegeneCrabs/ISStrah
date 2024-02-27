# Generated by Django 4.2.6 on 2024-02-20 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('client', '0004_alter_appointmentshealth_sum_insurance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointmentshealth',
            name='sum_insurance',
            field=models.CharField(choices=[(1.1, '100.000'), (1.3, '250.000'), (1.5, '500.000')], max_length=100, verbose_name='Сумма страхования'),
        ),
    ]
