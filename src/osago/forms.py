from django import forms

from src.authorization.models import CustomUser
from src.casco.models import CarModel, Brand
from src.osago.models import OsagoRecord, OsagoClaim, OsagoContract
from src.users.models import AgentSchedule, AppraiserSchedule


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


class OsagoClaimForm(forms.ModelForm):
    class Meta:
        model = OsagoClaim
        fields = ['description']


class OsagoClaimScheduleForm(forms.ModelForm):
    class Meta:
        model = OsagoClaim
        fields = ['availability_id']
        widgets = {
            'availability_id': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(OsagoClaimScheduleForm, self).__init__(*args, **kwargs)
        self.fields['availability_id'].queryset = AppraiserSchedule.objects.filter(available=True)


class OsagoRecordAgentForm(forms.ModelForm):
    class Meta:
        model = OsagoRecord
        fields = ['car_model', 'age', 'experience', 'insurance_cost', 'status', 'diagnostic_card',
                  'cost_expertise']
        widgets = {
            'car_model': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'experience': forms.NumberInput(attrs={'class': 'form-control'}),
            'insurance_cost': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'status': forms.HiddenInput(),
            'diagnostic_card': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'cost_expertise': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super(OsagoRecordAgentForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = 'in_progress'


class OsagoContractForm(forms.ModelForm):
    class Meta:
        model = OsagoContract
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
