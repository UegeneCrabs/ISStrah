from django import forms

from src.authorization.models import CustomUser
from src.life.models import LifeInsuranceRecord, HealthClaim, LifeInsuranceContract
from src.users.models import AgentSchedule, AppraiserSchedule


class LifeInsuranceForm(forms.ModelForm):
    class Meta:
        model = LifeInsuranceRecord
        fields = [
            'competition_participation', 'additional_sports', 'insurance_duration',
            'age_coefficient', 'sport_coverage', 'sum_insurance'
        ]
        widgets = {
            'competition_participation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'additional_sports': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'insurance_duration': forms.Select(attrs={'class': 'form-control'}),
            'age_coefficient': forms.Select(attrs={'class': 'form-control'}),
            'sport_coverage': forms.Select(attrs={'class': 'form-control'}),
            'sum_insurance': forms.Select(attrs={'class': 'form-control'}),
        }


class LifeInsuranceAgentForm(forms.ModelForm):
    class Meta:
        model = LifeInsuranceRecord
        fields = ['client', 'availability', 'competition_participation', 'additional_sports',
                  'insurance_duration', 'age_coefficient', 'sport_coverage', 'sum_insurance',
                  'insurance_cost', 'status']
        widgets = {
            'client': forms.Select(attrs={'class': 'form-control'}),
            'availability': forms.Select(attrs={'class': 'form-control'}),
            'competition_participation': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'additional_sports': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'insurance_duration': forms.Select(attrs={'class': 'form-control'}),
            'age_coefficient': forms.Select(attrs={'class': 'form-control'}),
            'sport_coverage': forms.Select(attrs={'class': 'form-control'}),
            'sum_insurance': forms.Select(attrs={'class': 'form-control'}),
            'insurance_cost': forms.NumberInput(attrs={'class': 'form-control'}),
            'status': forms.HiddenInput()  # Скрыть поле статус, так как оно уже установлено
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['availability'].queryset = AgentSchedule.objects.filter(available=True)
        self.fields['client'].queryset = CustomUser.objects.filter(user_type='users')
        self.fields['status'].initial = 'in_progress'
        self.fields['insurance_cost'].widget = forms.NumberInput(
            attrs={'class': 'form-control', 'readonly': 'readonly'})
        self.fields['status'].widget = forms.HiddenInput()


class LifeInsuranceSearchForm(forms.Form):
    search_query = forms.CharField(label='Поиск', required=False)
    insurance_duration = forms.ChoiceField(choices=[('', 'Любое')] + LifeInsuranceRecord.DURATION_CHOICES,
                                           label='Длительность страхования', required=False)
    age_coefficient = forms.ChoiceField(choices=[('', 'Любое')] + LifeInsuranceRecord.AGE_CHOICES,
                                        label='Возрастной коэффициент', required=False)
    sport_coverage = forms.ChoiceField(choices=[('', 'Любое')] + LifeInsuranceRecord.SPORT_COVERAGE_CHOICES,
                                       label='Категория спортивного покрытия', required=False)
    status = forms.ChoiceField(choices=[('', 'Любое')] + LifeInsuranceRecord.STATUS_CHOICES, label='Статус',
                               required=False)
    sum_insurance = forms.ChoiceField(choices=[('', 'Любое')] + LifeInsuranceRecord.SUM_INSURANCE_CHOICES,
                                      label='Сумма страхования', required=False)


class LifeRecordForm(forms.ModelForm):
    # Указываем виджеты для выбора значений
    competition_participation = forms.BooleanField(
        label="Участие в соревнованиях",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    additional_sports = forms.CharField(
        label="Дополнительные виды спорта",
        widget=forms.Textarea(attrs={'class': 'form-control'})
    )

    insurance_duration = forms.ChoiceField(
        label="Длительность страхования",
        choices=LifeInsuranceRecord.DURATION_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    age_coefficient = forms.ChoiceField(
        label="Возрастной коэффициент",
        choices=LifeInsuranceRecord.AGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    sport_coverage = forms.ChoiceField(
        label="Категория спортивного покрытия",
        choices=LifeInsuranceRecord.SPORT_COVERAGE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    sum_insurance = forms.ChoiceField(
        label="Сумма страхования",
        choices=LifeInsuranceRecord.SUM_INSURANCE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = LifeInsuranceRecord
        fields = ['competition_participation', 'additional_sports', 'insurance_duration',
                  'age_coefficient', 'sport_coverage', 'sum_insurance']


class LifeInsuranceScheduleForm(forms.ModelForm):
    class Meta:
        model = LifeInsuranceRecord
        fields = ['availability']
        widgets = {
            'availability': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(LifeInsuranceScheduleForm, self).__init__(*args, **kwargs)
        self.fields['availability'].queryset = AgentSchedule.objects.filter(available=True)


class LifeClaimForm(forms.ModelForm):
    class Meta:
        model = HealthClaim
        fields = ['description']


class HealthClaimScheduleForm(forms.ModelForm):
    class Meta:
        model = HealthClaim
        fields = ['schedule']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-control'})
        }

    def __init__(self, *args, **kwargs):
        super(HealthClaimScheduleForm, self).__init__(*args, **kwargs)
        self.fields['schedule'].queryset = AppraiserSchedule.objects.filter(available=True)


class LifeInsuranceContractForm(forms.ModelForm):
    class Meta:
        model = LifeInsuranceContract
        fields = ['start_date', 'end_date']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
