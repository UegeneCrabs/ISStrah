from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class CustomUser(AbstractUser):
    surname = models.CharField(max_length=100, verbose_name="Фамилия")
    name = models.CharField(max_length=100, verbose_name="Имя")
    secondname = models.CharField(max_length=100, verbose_name="Отчество")
    email = models.EmailField(verbose_name='Почтовый адрес', unique=True)
    phone_number = models.CharField(max_length=100, verbose_name="Номер телефона", unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    USER_TYPE_CHOICES = [
        ('agent', 'Страховой агент'),
        ('users', 'Страховщик'),
        ('appraiser', 'Оценщик'),
    ]

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name="Тип пользователя", null=True,
                                 blank=True)
    experience = models.CharField(max_length=100, verbose_name="Опыт", null=True, blank=True)
    position = models.CharField(max_length=100, verbose_name="Должность", null=True, blank=True)

    def __str__(self):
        return f"--- {self.email} --- {self.surname} {self.name} {self.secondname} - {self.get_user_type_display()}."



