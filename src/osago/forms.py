from django import forms

from src.casco.models import CarModel, Brand
from src.osago.models import OsagoRecord
from src.users.models import AgentSchedule


# class InsuranceCalculatorForm(forms.Form):
#     # Поля для выбора марки авто, модели авто и года выпуска
#     brand = forms.CharField(label='Марка авто', max_length=100)
#     model = forms.CharField(label='Модель авто', max_length=100)
#     car_year = forms.IntegerField(label='Год выпуска', min_value=1900, max_value=2025)
#
#     # Поле для выбора количества лошадиных сил
#     horse_power = forms.IntegerField(label='Лошадиные силы')
#
#     # Поле для выбора КО
#     DRIVER_CHOICES = [
#         ('one_person', 'Один человек'),
#         ('unlimited', 'Неограниченное количество'),
#     ]
#     driver_option = forms.ChoiceField(label='Количество лиц допущенных к управлению', choices=DRIVER_CHOICES)
#
#     # Поля для записи возраста и стажа клиента
#     age = forms.IntegerField(label='Возраст')
#     experience = forms.IntegerField(label='Стаж')


# class OsagoRecordForm(forms.ModelForm):
#     number_of_drivers_choices = [
#         ('limited', 'Ограниченный список'),
#         ('unlimited', 'Неограниченный список')
#     ]
#     number_of_drivers = forms.ChoiceField(choices=number_of_drivers_choices, label="Тип списка водителей", widget=forms.RadioSelect)
#
#     class Meta:
#         model = OsagoRecord
#         fields = ['car_model', 'age', 'experience', 'number_of_drivers']
#         widgets = {
#             'car_model': forms.Select(attrs={'class': 'form-control'}),
#             'age': forms.NumberInput(attrs={'class': 'form-control'}),
#             'experience': forms.NumberInput(attrs={'class': 'form-control'}),
#         }
#
#     def __init__(self, *args, **kwargs):
#         user = kwargs.pop('user', None)
#         super().__init__(*args, **kwargs)
#         if user:
#             self.instance.client = user
#         self.fields['car_model'].queryset = CarModel.objects.all()
#
#     def clean(self):
#         cleaned_data = super().clean()
#         car_model = cleaned_data.get('car_model')
#         age = cleaned_data.get('age')
#         experience = cleaned_data.get('experience')
#         number_of_drivers = cleaned_data.get('number_of_drivers')
#
#         kt = 1.8
#         km = self.calculate_km(car_model.horsepower)
#         kvs = self.calculate_kvs(age, experience)
#         do = self.calculate_do(number_of_drivers)
#         cc = self.calculate_cc(car_model.year)
#         tariff = 5000
#
#         insurance_cost = tariff * kt * km * kvs * do * cc
#         self.instance.insurance_cost = insurance_cost
#
#     def calculate_km(self, horsepower):
#         if horsepower < 50:
#             return 0.6
#         elif horsepower < 70:
#             return 1
#         elif horsepower < 100:
#             return 1.1
#         elif horsepower < 120:
#             return 1.2
#         elif horsepower < 150:
#             return 1.4
#         else:
#             return 1.6
#
#     def calculate_kvs(self, age, experience):
#         if age <= 22 and experience <= 3:
#             return 1.8
#         elif age > 22 and experience <= 3:
#             return 1.7
#         elif age <= 22 and experience > 3:
#             return 1.6
#         else:
#             return 1
#
#     def calculate_do(self, number_of_drivers_type):
#         if number_of_drivers_type == 'limited':
#             return 1
#         elif number_of_drivers_type == 'unlimited':
#             return 2
#
#     def calculate_cc(self, year):
#         current_year = 2023
#         return 1 + 0.1 * (current_year - year)

class OsagoSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)


class CarForm(forms.Form):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label="Марка автомобиля")
    model_name = forms.ChoiceField(choices=[], label="Название модели")
    year = forms.ChoiceField(choices=[], label="Год выпуска")
    horsepower = forms.ChoiceField(choices=[], label="Лошадиные силы")
    age = forms.IntegerField(label="Возраст")
    experience = forms.IntegerField(label="Стаж")

    def __init__(self, *args, **kwargs):
        super(CarForm, self).__init__(*args, **kwargs)
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model_name'].choices = [(model['model_name'], model['model_name']) for model in
                                                     CarModel.objects.filter(brand_id=brand_id).values(
                                                         'model_name').distinct()]
            except (ValueError, TypeError):
                pass

        if 'model_name' in self.data and 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                model_name = self.data.get('model_name')
                self.fields['year'].choices = [(model['year'], model['year']) for model in
                                               CarModel.objects.filter(brand_id=brand_id, model_name=model_name).values(
                                                   'year').distinct()]
            except (ValueError, TypeError):
                pass

        if 'year' in self.data and 'model_name' in self.data and 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                model_name = self.data.get('model_name')
                year = int(self.data.get('year'))
                self.fields['horsepower'].choices = [(model['horsepower'], model['horsepower']) for model in
                                                     CarModel.objects.filter(brand_id=brand_id, model_name=model_name,
                                                                             year=year).values('horsepower').distinct()]
            except (ValueError, TypeError):
                pass


import logging

logger = logging.getLogger(__name__)


class OsagoRecordForm(forms.ModelForm):
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), label="Марка автомобиля",
                                   widget=forms.Select(attrs={'class': 'form-control'}), empty_label="-------")
    model_name = forms.ChoiceField(choices=[('', '-------')], label="Название модели",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    year = forms.ChoiceField(choices=[('', '-------')], label="Год выпуска",
                             widget=forms.Select(attrs={'class': 'form-control'}))
    horsepower = forms.ChoiceField(choices=[('', '-------')], label="Лошадиные силы",
                                   widget=forms.Select(attrs={'class': 'form-control'}))
    age = forms.IntegerField(label="Возраст", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    experience = forms.IntegerField(label="Стаж", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = OsagoRecord
        fields = ['brand', 'model_name', 'year', 'horsepower', 'age', 'experience']

    def __init__(self, *args, **kwargs):
        super(OsagoRecordForm, self).__init__(*args, **kwargs)
        try:
            if 'brand' in self.data:
                brand_id = int(self.data.get('brand'))
                self.fields['model_name'].choices += [(model['model_name'], model['model_name']) for model in
                                                      CarModel.objects.filter(brand_id=brand_id).values(
                                                          'model_name').distinct()]

            if 'model_name' in self.data and 'brand' in self.data:
                brand_id = int(self.data.get('brand'))
                model_name = self.data.get('model_name')
                self.fields['year'].choices += [(model['year'], model['year']) for model in
                                                CarModel.objects.filter(brand_id=brand_id,
                                                                        model_name=model_name).values(
                                                    'year').distinct()]

            if 'year' in self.data and 'model_name' in self.data and 'brand' in self.data:
                brand_id = int(self.data.get('brand'))
                model_name = self.data.get('model_name')
                year = int(self.data.get('year'))
                self.fields['horsepower'].choices += [(model['horsepower'], model['horsepower']) for model in
                                                      CarModel.objects.filter(brand_id=brand_id, model_name=model_name,
                                                                              year=year).values(
                                                          'horsepower').distinct()]
        except (ValueError, TypeError) as e:
            logger.error(f"Error initializing form fields: {e}")


class OsagoScheduleForm(forms.ModelForm):
    class Meta:
        model = OsagoRecord
        fields = ['schedule']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(OsagoScheduleForm, self).__init__(*args, **kwargs)
        self.fields['schedule'].queryset = AgentSchedule.objects.filter(available=True)
