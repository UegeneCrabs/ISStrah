# Generated by Django 4.2.6 on 2024-02-20 17:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentsCar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('brand', models.CharField(max_length=100, verbose_name='Марка авто')),
                ('model', models.CharField(max_length=100, verbose_name='Модель авто')),
                ('car_year', models.IntegerField(verbose_name='Год выпуска')),
                ('horse_power', models.IntegerField(verbose_name='Лошадиные силы')),
                ('driver_option', models.CharField(choices=[('one_person', 'Один человек'), ('unlimited', 'Неограниченное количество')], max_length=100, verbose_name='Количество лиц допущенных к управлению')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('experience', models.IntegerField(verbose_name='Стаж')),
                ('insurance_cost', models.FloatField(verbose_name='Стоимость страховки')),
            ],
        ),
        migrations.CreateModel(
            name='Availability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('available', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentsHealth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('participation_in_competition', models.BooleanField(default=False, verbose_name='Участие в соревнованиях')),
                ('additional_sports', models.CharField(default=False, max_length=100, verbose_name='Дополнительные виды спорта')),
                ('duration', models.CharField(choices=[(1, '1 год'), (1.2, '6 месяцев'), (1.3, '3 месяца'), (1.5, '1 месяц')], max_length=100, verbose_name='Длительность страхования')),
                ('age_coefficient', models.CharField(choices=[(1, 'От 3 до 17 лет'), (1.5, 'От 18 до 35 лет'), (1.8, 'От 36 до 65 лет')], max_length=100, verbose_name='Возрастной коэффициент')),
                ('sport_coverage', models.CharField(choices=[(1.2, 'Обычный'), (1.4, 'Расширенный')], max_length=100, verbose_name='Категория спортивного покрытия')),
                ('sum_insurance', models.CharField(choices=[(1.1, '100.000'), (1.3, '250.000'), (1.5, '500.000')], max_length=100, verbose_name='Сумма страхования')),
                ('insurance_cost', models.FloatField(verbose_name='Стоимость страховки')),
                ('available', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='client.availability', verbose_name='Время')),
            ],
        ),
    ]
