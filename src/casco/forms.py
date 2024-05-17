from django import forms

from src.casco.models import Brand, CarModel, CascoRecord
from src.users.models import AgentSchedule


class CarSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)
    coverage = forms.ChoiceField(choices=[('', 'Любое')] + list(CascoRecord.COVERAGE_CHOICES), label='Покрытие',
                                 required=False)
    repair_type = forms.ChoiceField(choices=[('', 'Любое')] + list(CascoRecord.REPAIR_TYPE_CHOICES),
                                    label='Тип ремонта', required=False)
    status = forms.ChoiceField(choices=[('', 'Любое')] + list(CascoRecord.STATUS_CHOICES), label='Статус',
                               required=False)
    cost_guarantee = forms.ChoiceField(choices=[('', 'Любое'), ('True', 'Включена'), ('False', 'Не включена')],
                                       label='Гарантия стоимости', required=False)


class CarCascoForm(forms.Form):
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

    COVERAGE_CHOICES = (
        ('full', 'Полное покрытие'),
        ('theft_destruction', 'Угон + гибель авто'),
        ('damage_destruction', 'Ущерб + гибель авто'),
    )
    coverage = forms.ChoiceField(choices=COVERAGE_CHOICES, label="Покрытие",
                                 widget=forms.Select(attrs={'class': 'form-control'}))

    REPAIR_TYPE_CHOICES = (
        ('dealer', 'Дилерский центр'),
        ('specialized_service', 'Специализированный сервис'),
        ('express_repair', 'Экспресс-ремонт'),
    )
    repair_type = forms.ChoiceField(choices=REPAIR_TYPE_CHOICES, label="Тип ремонта",
                                    widget=forms.Select(attrs={'class': 'form-control'}))

    mileage = forms.IntegerField(label="Пробег", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cost_guarantee = forms.BooleanField(label="Гарантия стоимости", required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    car_cost = forms.DecimalField(label="Стоимость авто", max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(CarCascoForm, self).__init__(*args, **kwargs)
        if 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                self.fields['model_name'].choices += [(model['model_name'], model['model_name']) for model in
                                                      CarModel.objects.filter(brand_id=brand_id).values(
                                                          'model_name').distinct()]
            except (ValueError, TypeError):
                pass

        if 'model_name' in self.data and 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                model_name = self.data.get('model_name')
                self.fields['year'].choices += [(model['year'], model['year']) for model in
                                                CarModel.objects.filter(brand_id=brand_id,
                                                                        model_name=model_name).values(
                                                    'year').distinct()]
            except (ValueError, TypeError):
                pass

        if 'year' in self.data and 'model_name' in self.data and 'brand' in self.data:
            try:
                brand_id = int(self.data.get('brand'))
                model_name = self.data.get('model_name')
                year = int(self.data.get('year'))
                self.fields['horsepower'].choices += [(model['horsepower'], model['horsepower']) for model in
                                                      CarModel.objects.filter(brand_id=brand_id, model_name=model_name,
                                                                              year=year).values(
                                                          'horsepower').distinct()]
            except (ValueError, TypeError):
                pass


import logging

logger = logging.getLogger(__name__)


class CascoRecordForm(forms.ModelForm):
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
    coverage = forms.ChoiceField(choices=CascoRecord.COVERAGE_CHOICES, label="Покрытие",
                                 widget=forms.Select(attrs={'class': 'form-control'}))
    repair_type = forms.ChoiceField(choices=CascoRecord.REPAIR_TYPE_CHOICES, label="Тип ремонта",
                                    widget=forms.Select(attrs={'class': 'form-control'}))
    mileage = forms.IntegerField(label="Пробег", widget=forms.NumberInput(attrs={'class': 'form-control'}))
    cost_guarantee = forms.BooleanField(label="Гарантия стоимости", required=False,
                                        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}))
    car_cost = forms.DecimalField(label="Стоимость авто", max_digits=10, decimal_places=2,
                                  widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = CascoRecord
        fields = ['brand', 'model_name', 'year', 'horsepower', 'age', 'experience', 'coverage', 'repair_type',
                  'mileage', 'cost_guarantee', 'car_cost']

    def __init__(self, *args, **kwargs):
        super(CascoRecordForm, self).__init__(*args, **kwargs)
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


class CascoScheduleForm(forms.ModelForm):
    class Meta:
        model = CascoRecord
        fields = ['schedule']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(CascoScheduleForm, self).__init__(*args, **kwargs)
        self.fields['schedule'].queryset = AgentSchedule.objects.filter(available=True)
