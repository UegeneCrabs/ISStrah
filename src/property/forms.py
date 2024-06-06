from django import forms

from src.property.models import HomeInsuranceRecord, HomeInsuranceClaim, HomeInsuranceContract
from src.users.models import AgentSchedule, AppraiserSchedule


class HomeInsuranceForm(forms.ModelForm):
    class Meta:
        model = HomeInsuranceRecord
        fields = [
            'city', 'street', 'house', 'apartment', 'interior_finish',
            'structural_elements', 'civil_liability', 'household_property',
            'additional_protection', 'war_risk', 'neighbor_repair_liability', 'atmospheric_impact'
        ]
        widgets = {
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'street': forms.TextInput(attrs={'class': 'form-control'}),
            'house': forms.TextInput(attrs={'class': 'form-control'}),
            'apartment': forms.TextInput(attrs={'class': 'form-control'}),
            'interior_finish': forms.Select(attrs={'class': 'form-control'}),
            'structural_elements': forms.Select(attrs={'class': 'form-control'}),
            'civil_liability': forms.Select(attrs={'class': 'form-control'}),
            'household_property': forms.Select(attrs={'class': 'form-control'}),
            'additional_protection': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'war_risk': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'neighbor_repair_liability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'atmospheric_impact': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class HomeInsuranceSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)
    additional_protection = forms.ChoiceField(choices=[('', 'Любое'), (True, 'Да'), (False, 'Нет')],
                                              label='Дополнительная защита', required=False)
    war_risk = forms.ChoiceField(choices=[('', 'Любое'), (True, 'Да'), (False, 'Нет')], label='Риск военных действий',
                                 required=False)
    neighbor_repair_liability = forms.ChoiceField(choices=[('', 'Любое'), (True, 'Да'), (False, 'Нет')],
                                                  label='Ответственность перед соседями при ремонте', required=False)
    atmospheric_impact = forms.ChoiceField(choices=[('', 'Любое'), (True, 'Да'), (False, 'Нет')],
                                           label='Воздействие атмосферных осадков', required=False)
    status = forms.ChoiceField(choices=[('', 'Любое')] + HomeInsuranceRecord.STATUS_CHOICES, label='Статус',
                               required=False)


class HomeRecordForm(forms.ModelForm):
    city = forms.CharField(
        label="Город",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    street = forms.CharField(
        label="Улица",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    house = forms.CharField(
        label="Дом",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    apartment = forms.CharField(
        label="Квартира",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )

    interior_finish = forms.ChoiceField(
        label="Внутренняя отделка",
        choices=HomeInsuranceRecord.CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    structural_elements = forms.ChoiceField(
        label="Конструктивные элементы",
        choices=HomeInsuranceRecord.CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    civil_liability = forms.ChoiceField(
        label="Гражданская ответственность",
        choices=HomeInsuranceRecord.CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    household_property = forms.ChoiceField(
        label="Домашнее имущество",
        choices=HomeInsuranceRecord.CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    additional_protection = forms.BooleanField(
        label="Дополнительная защита",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    war_risk = forms.BooleanField(
        label="Риск военных действий",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    neighbor_repair_liability = forms.BooleanField(
        label="Ответственность перед соседями при ремонте",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    atmospheric_impact = forms.BooleanField(
        label="Воздействие атмосферных осадков",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    class Meta:
        model = HomeInsuranceRecord
        fields = [
            'city', 'street', 'house', 'apartment',
            'interior_finish', 'structural_elements', 'civil_liability', 'household_property',
            'additional_protection', 'war_risk', 'neighbor_repair_liability', 'atmospheric_impact'
        ]


class ScheduleForm(forms.Form):
    schedule_time = forms.ModelChoiceField(
        queryset=AgentSchedule.objects.filter(available=True),
        label="Выберите время",
        empty_label=None,
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class HomeClaimForm(forms.ModelForm):
    class Meta:
        model = HomeInsuranceClaim
        fields = ['description']


class HomeInsuranceClaimScheduleForm(forms.ModelForm):
    class Meta:
        model = HomeInsuranceClaim
        fields = ['availability_id']
        widgets = {
            'availability_id': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(HomeInsuranceClaimScheduleForm, self).__init__(*args, **kwargs)
        self.fields['availability_id'].queryset = AppraiserSchedule.objects.filter(available=True)


class HomeInsuranceContractForm(forms.ModelForm):
    class Meta:
        model = HomeInsuranceContract
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
