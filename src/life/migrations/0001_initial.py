# Generated by Django 4.2.6 on 2024-05-12 12:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HealthClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обращения')),
                ('description', models.TextField(verbose_name='Описание случая')),
                ('payout_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма выплаты')),
                ('processed', models.BooleanField(default=False, verbose_name='Проработана')),
                ('appraiser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Страховой оценщик')),
            ],
            options={
                'verbose_name': 'Обращение по страхованию здоровья',
                'verbose_name_plural': 'Обращения по страхованию здоровья',
            },
        ),
        migrations.CreateModel(
            name='LifePayoutAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage_character', models.TextField(verbose_name='Характер повреждения')),
                ('percentage_of_insurance_amount', models.FloatField(verbose_name='Процент от страховой суммы')),
            ],
            options={
                'verbose_name': 'Оценка выплаты по страхованию жизни',
                'verbose_name_plural': 'Оценки выплат по страхованию жизни',
            },
        ),
        migrations.CreateModel(
            name='LifeInsuranceRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('competition_participation', models.BooleanField(verbose_name='Участие в соревнованиях')),
                ('additional_sports', models.TextField(verbose_name='Дополнительные виды спорта')),
                ('insurance_duration', models.FloatField(choices=[(1, '1 год'), (1.2, '6 месяцев'), (1.3, '3 месяца'), (1.5, '1 месяц')], max_length=100, verbose_name='Длительность страхования')),
                ('age_coefficient', models.FloatField(choices=[(1, 'От 3 до 17 лет'), (1.5, 'От 18 до 35 лет'), (1.8, 'От 36 до 65 лет')], max_length=100, verbose_name='Возрастной коэффициент')),
                ('sport_coverage', models.FloatField(choices=[(1.2, 'Обычный'), (1.4, 'Расширенный')], max_length=100, verbose_name='Категория спортивного покрытия')),
                ('sum_insurance', models.FloatField(choices=[(1.1, '100.000'), (1.3, '250.000'), (1.5, '500.000')], max_length=100, verbose_name='Сумма страхования')),
                ('insurance_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость страховки')),
                ('processed', models.BooleanField(default=False, verbose_name='Проработана')),
                ('availability', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.agentschedule', verbose_name='Доступность')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
            ],
            options={
                'verbose_name': 'Запись на прием по страхованию жизни',
                'verbose_name_plural': 'Записи на прием по страхованию жизни',
            },
        ),
        migrations.CreateModel(
            name='LifeInsuranceContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conclusion_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата заключения')),
                ('start_date', models.DateField(verbose_name='Начало действия')),
                ('end_date', models.DateField(verbose_name='Конец действия')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Агент')),
                ('record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='life.lifeinsurancerecord', verbose_name='Запись')),
            ],
            options={
                'verbose_name': 'Договор страхования жизни',
                'verbose_name_plural': 'Договоры страхования жизни',
            },
        ),
        migrations.CreateModel(
            name='LifeClaimAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('life_assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='life.lifepayoutassessment', verbose_name='Оценка жизни')),
                ('life_claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='life.healthclaim', verbose_name='Обращение жизни')),
            ],
            options={
                'verbose_name': 'Связь обращения и оценки по страхованию жизни',
                'verbose_name_plural': 'Связи обращений и оценок по страхованию жизни',
            },
        ),
        migrations.AddField(
            model_name='healthclaim',
            name='insurance_contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='life.lifeinsurancecontract', verbose_name='Договор страхования здоровья'),
        ),
        migrations.AddField(
            model_name='healthclaim',
            name='schedule',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.appraiserschedule', verbose_name='Расписание оценщика'),
        ),
    ]
