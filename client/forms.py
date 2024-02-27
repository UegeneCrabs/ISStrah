from django import forms
from .models import Availability, AppointmentsCar, AppointmentsHealth


class DateSelectionForm(forms.Form):
    available_dates = forms.ModelChoiceField(queryset=Availability.objects.filter(available=True),
                                             label='Available Dates')


class AppointmentsCarForm(forms.ModelForm):
    class Meta:
        model = AppointmentsCar
        fields = ['brand', 'model', 'car_year', 'horse_power',
                  'driver_option', 'age', 'experience']


class AppointmentsHealthForm(forms.ModelForm):
    class Meta:
        model = AppointmentsHealth
        fields = ['participation_in_competition', 'additional_sports', 'duration', 'age_coefficient', 'sport_coverage',
                  'sum_insurance']


class InsuranceCalculatorForm(forms.Form):
    # Поля для выбора марки авто, модели авто и года выпуска
    brand = forms.CharField(label='Марка авто', max_length=100)
    model = forms.CharField(label='Модель авто', max_length=100)
    car_year = forms.IntegerField(label='Год выпуска', min_value=1900, max_value=2025)

    # Поле для выбора количества лошадиных сил
    horse_power = forms.IntegerField(label='Лошадиные силы')

    # Поле для выбора КО
    DRIVER_CHOICES = [
        ('one_person', 'Один человек'),
        ('unlimited', 'Неограниченное количество'),
    ]
    driver_option = forms.ChoiceField(label='Количество лиц допущенных к управлению', choices=DRIVER_CHOICES)

    # Поля для записи возраста и стажа клиента
    age = forms.IntegerField(label='Возраст')
    experience = forms.IntegerField(label='Стаж')


class HealthInsuranceCalculatorForm(forms.Form):
    # Поле для выбора КД
    DURATION_CHOICES = [
        (1, '1 год'),
        (1.2, '6 месяцев'),
        (1.3, '3 месяца'),
        (1.5, '1 месяц'),
    ]
    duration = forms.ChoiceField(label='Длительность страхования', choices=DURATION_CHOICES)

    # Поле для выбора КВ
    AGE_CHOICES = [
        (1, 'От 3 до 17 лет'),
        (1.5, 'От 18 до 35 лет'),
        (1.8, 'От 36 до 65 лет'),
    ]
    age_coefficient = forms.ChoiceField(label='Возрастной коэффициент', choices=AGE_CHOICES)

    # Поле для выбора КСП
    SPORT_COVERAGE_CHOICES = [
        (1.2, 'Обычный'),
        (1.4, 'Расширенный'),
    ]
    sport_coverage = forms.ChoiceField(label='Категория спортивного покрытия', choices=SPORT_COVERAGE_CHOICES)

    SUM_INSURANCE_CHOICES = [
        (1.1, '100.000'),
        (1.3, '250.000'),
        (1.5, '500.000'),
    ]
    sum_insurance = forms.ChoiceField(label='Сумма страхования', choices=SUM_INSURANCE_CHOICES)
    # Поле для добавления ДВС
    additional_sports = forms.CharField(label='Дополнительные виды спорта', required=False)

    # Поле для выбора УС
    participation_in_competition = forms.BooleanField(label='Участие в соревнованиях', required=False)
