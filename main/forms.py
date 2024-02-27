from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password1', 'password2', 'surname', 'name', 'secondname', 'phone_number']
        widgets = {
            "username": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Логин'
            }),
            "email": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Электронная почта'
            }),
            "password1": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Пароль'
            }),
            "password2": forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Повторите пароль'
            }),
            "name": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            "surname": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            "secondname": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Отчество'
            }),
            "phone_number": forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер телефона'
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        # Автоматически устанавливаем тип пользователя как "client"
        cleaned_data['user_type'] = 'client'
        return cleaned_data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from .models import CustomUser
#
#
# class CustomUserCreationForm(UserCreationForm):
#     USER_TYPE_CHOICES = [
#         ('agent', 'Страховой агент'),
#         ('client', 'Страховщик'),
#     ]
#
#     user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.RadioSelect(), label='Тип пользователя')
#     experience = forms.CharField(max_length=100, required=False, label='Опыт работы')
#     position = forms.CharField(max_length=100, required=False, label='Должность')
#
#     class Meta:
#         model = CustomUser
#         fields = ['email', 'username', 'password1', 'password2', 'surname', 'name',
#                   'secondname', 'phone_number', 'user_type', 'experience', 'position']
#         widgets = {
#             "email": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Электронная почта'
#             }),
#             "username": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Логин'
#             }),
#             "password1": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Пароль'
#             }),
#             "password2": forms.PasswordInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Повторите пароль'
#             }),
#             "surname": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Фамилия'
#             }),
#             "name": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Имя'
#             }),
#             "secondname": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Отчество'
#             }),
#             "phone_number": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Номер телефона'
#             }),
#             "experience": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Опыт работы'
#             }),
#             "position": forms.TextInput(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Должность'
#             }),
#         }
#
#     def clean(self):
#         cleaned_data = super().clean()
#         user_type = cleaned_data.get('user_type')
#         experience = cleaned_data.get('experience')
#         position = cleaned_data.get('position')
#
#         if user_type == 'client' and (experience or position):
#             raise forms.ValidationError('Поле "Опыт работы" и "Должность" заполняются только для страховых агентов.')
#         return cleaned_data


# class CarSelectionForm(forms.Form):
#     brand = forms.ChoiceField(label='Марка авто', choices=[], required=True)
#     model = forms.ChoiceField(label='Модель авто', choices=[], required=True)
#     horse_power = forms.ChoiceField(label='Лошадиные силы', choices=[], required=True)
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['model'].choices = []
#         self.fields['horse_power'].choices = []
#
#         # Заполнение полей бренда
#         brands = Car.objects.values_list('brand', 'brand').distinct()
#         self.fields['brand'].choices = brands

# class CarSelectionForm(forms.Form):
#     brand = forms.ModelChoiceField(queryset=Car.objects.values_list('brand', flat=True).distinct(),
#                                    label='Марка авто')
#     model = forms.ChoiceField(choices=[], label='Модель авто')
#     horse_power = forms.IntegerField(label='Лошадиные силы')
#
#     def __init__(self, *args, **kwargs):
#         super(CarSelectionForm, self).__init__(*args, **kwargs)
#         if 'brand' in self.data:
#             try:
#                 brand_id = int(self.data.get('brand'))
#                 models = Car.objects.filter(brand=brand_id).values_list('model', 'model')
#                 self.fields['model'].choices = models
#             except (ValueError, TypeError):
#                 pass
