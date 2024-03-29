# Generated by Django 4.2.6 on 2024-02-27 05:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('client', '0011_alter_appointmentshealth_additional_sports_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppealHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.FloatField(null=True, verbose_name='Сумма выплаты')),
                ('nature_damage', models.CharField(max_length=255, null=True, verbose_name='Опись повреждения')),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appeal_agent_health', to=settings.AUTH_USER_MODEL, verbose_name='Договор')),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.contracthealth', verbose_name='Договор')),
                ('payment_table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.paymenttablehealth', verbose_name='Таблица выплат')),
            ],
        ),
        migrations.CreateModel(
            name='AppealCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_amount', models.FloatField(null=True, verbose_name='Сумма выплаты')),
                ('nature_damage', models.CharField(max_length=255, null=True, verbose_name='Опись повреждения')),
                ('agent', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='appeal_agent_car', to=settings.AUTH_USER_MODEL, verbose_name='Договор')),
                ('contract_car', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.contractcar', verbose_name='Договор')),
                ('payment_table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='client.paymenttablecar', verbose_name='Таблица выплат')),
            ],
        ),
    ]
