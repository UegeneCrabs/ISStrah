from django.db import models

from src.authorization.models import CustomUser


class AgentSchedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    available = models.BooleanField()
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Агент")

    class Meta:
        verbose_name = "Расписание агента"
        verbose_name_plural = "Расписание агентов"

    def __str__(self):
        return f"{self.date} - {self.time}: {'Free' if self.available else 'Booked'}"


class AppraiserSchedule(models.Model):
    date = models.DateField()
    time = models.TimeField()
    available = models.BooleanField()
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Оценщик")

    class Meta:
        verbose_name = "Расписание Оценщика"
        verbose_name_plural = "Расписание Оценщиков"

    def __str__(self):
        return f"{self.date} - {self.time}: {'Free' if self.available else 'Booked'}"
