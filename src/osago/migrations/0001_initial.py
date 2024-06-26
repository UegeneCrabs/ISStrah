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
        ('casco', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OsagoAdditionalDriver',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=255, verbose_name='Фамилия')),
                ('first_name', models.CharField(max_length=255, verbose_name='Имя')),
                ('patronymic', models.CharField(max_length=255, verbose_name='Отчество')),
                ('birth_date', models.DateField(verbose_name='Дата рождения')),
            ],
            options={
                'verbose_name': 'Дополнительный водитель ОСАГО',
                'verbose_name_plural': 'Дополнительные водители ОСАГО',
            },
        ),
        migrations.CreateModel(
            name='OsagoAutoPayoutAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage_character', models.TextField(verbose_name='Характер повреждения')),
                ('percentage_of_insurance_amount', models.FloatField(verbose_name='Процент от страховой суммы')),
            ],
            options={
                'verbose_name': 'Оценка выплаты ОСАГО-Авто',
                'verbose_name_plural': 'Оценки выплат ОСАГО-Авто',
            },
        ),
        migrations.CreateModel(
            name='OsagoClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата обращения')),
                ('description', models.TextField(verbose_name='Описание случая')),
                ('payout_amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма выплаты')),
                ('processed', models.BooleanField(default=False, verbose_name='Проработана')),
                ('appraiser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Страховой оценщик')),
                ('availability_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='users.appraiserschedule', verbose_name='Расписание Оценщика')),
            ],
            options={
                'verbose_name': 'Обращение ОСАГО',
                'verbose_name_plural': 'Обращения ОСАГО',
            },
        ),
        migrations.CreateModel(
            name='OsagoLifePayoutAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('damage_character', models.TextField(verbose_name='Характер повреждения')),
                ('percentage_of_insurance_amount', models.FloatField(verbose_name='Процент от страховой суммы')),
            ],
            options={
                'verbose_name': 'Оценка выплаты ОСАГО-Жизнь',
                'verbose_name_plural': 'Оценки выплат ОСАГО-Жизнь',
            },
        ),
        migrations.CreateModel(
            name='OsagoRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_drivers', models.IntegerField(verbose_name='Количество лиц, допущенных к управлению')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('experience', models.IntegerField(verbose_name='Стаж')),
                ('insurance_cost', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость страховки')),
                ('processed', models.BooleanField(default=False, verbose_name='Проработана')),
                ('diagnostic_card', models.BooleanField(default=False, verbose_name='Карта диагностики')),
                ('cost_expertise', models.BooleanField(default=False, verbose_name='Экспертиза стоимости')),
                ('car_model', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='casco.carmodel', verbose_name='Модель автомобиля')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Клиент')),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.agentschedule', verbose_name='Расписание агента')),
            ],
            options={
                'verbose_name': 'Запись на прием ОСАГО',
                'verbose_name_plural': 'Записи на прием ОСАГО',
            },
        ),
        migrations.CreateModel(
            name='OsagoContract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conclusion_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='Дата заключения')),
                ('start_date', models.DateField(verbose_name='Начало действия')),
                ('end_date', models.DateField(verbose_name='Конец действия')),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Агент')),
                ('osago_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagorecord', verbose_name='Запись ОСАГО')),
            ],
            options={
                'verbose_name': 'Договор ОСАГО',
                'verbose_name_plural': 'Договора ОСАГО',
            },
        ),
        migrations.CreateModel(
            name='OsagoClaimLifeAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osago_claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagoclaim', verbose_name='Обращение ОСАГО')),
                ('osago_life_assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagolifepayoutassessment', verbose_name='Оценка ОСАГО-Жизнь')),
            ],
            options={
                'verbose_name': 'Обращение - Оценка ОСАГО-Жизнь',
                'verbose_name_plural': 'Обращения - Оценки ОСАГО-Жизнь',
            },
        ),
        migrations.CreateModel(
            name='OsagoClaimAutoAssessment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('osago_auto_assessment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagoautopayoutassessment', verbose_name='Оценка ОСАГО-Авто')),
                ('osago_claim', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagoclaim', verbose_name='Обращение ОСАГО')),
            ],
            options={
                'verbose_name': 'Обращение - Оценка ОСАГО-Авто',
                'verbose_name_plural': 'Обращения - Оценки ОСАГО-Авто',
            },
        ),
        migrations.AddField(
            model_name='osagoclaim',
            name='osago_contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagocontract', verbose_name='Договор ОСАГО'),
        ),
        migrations.CreateModel(
            name='DriversOsagoRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagoadditionaldriver', verbose_name='Водитель')),
                ('osago_record', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='osago.osagorecord', verbose_name='Запись ОСАГО')),
            ],
            options={
                'verbose_name': 'Водитель - Запись ОСАГО',
                'verbose_name_plural': 'Водители - Записи ОСАГО',
            },
        ),
    ]
