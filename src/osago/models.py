from django.db import models
from django.utils import timezone

from src.authorization.models import CustomUser
from src.casco.models import CarModel
from src.users.models import AgentSchedule, AppraiserSchedule


# Запись на прием ОСАГО
class OsagoRecord(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")
    schedule = models.ForeignKey(AgentSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name="Расписание агента")
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name="Модель автомобиля")
    age = models.IntegerField(verbose_name="Возраст")
    experience = models.IntegerField(verbose_name="Стаж")
    insurance_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость страховки")
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )
    diagnostic_card = models.BooleanField(default=False, verbose_name="Карта диагностики")
    cost_expertise = models.BooleanField(default=False, verbose_name="Экспертиза стоимости")

    class Meta:
        verbose_name = "Запись на прием ОСАГО"
        verbose_name_plural = "Записи на прием ОСАГО"

    def __str__(self):
        return f"Запись ОСАГО для {self.client.name} - {self.car_model}. Статус: {self.status}"


# Договор страхования ОСАГО
class OsagoContract(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Агент")
    osago_record = models.ForeignKey(OsagoRecord, on_delete=models.CASCADE, verbose_name="Запись ОСАГО")
    conclusion_date = models.DateTimeField(default=timezone.now, verbose_name="Дата заключения")
    start_date = models.DateField(verbose_name="Начало действия")
    end_date = models.DateField(verbose_name="Конец действия")

    class Meta:
        verbose_name = "Договор ОСАГО"
        verbose_name_plural = "Договора ОСАГО"

    def __str__(self):
        return f"Договор ОСАГО от {self.start_date} до {self.end_date} (Агент: {self.agent})"


class DamageThemeOsagoAuto(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тематики")

    class Meta:
        verbose_name = "Тема повреждения ОСАГО АВТО"
        verbose_name_plural = "Темы повреждений ОСАГО АВТО"

    def __str__(self):
        return self.name


class DamageThemeOsagoLife(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тематики")

    class Meta:
        verbose_name = "Тема повреждения ОСАГО Жизнь"
        verbose_name_plural = "Темы повреждений ОСАГО Жизнь"

    def __str__(self):
        return self.name


# Оценка выплаты ОСАГО-Авто
class OsagoAutoPayoutAssessment(models.Model):
    damage_character = models.TextField(verbose_name="Характер повреждения")
    percentage_of_insurance_amount = models.FloatField(verbose_name="Процент от страховой суммы")
    theme = models.ForeignKey(DamageThemeOsagoAuto, null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name="Тематика повреждения")

    class Meta:
        verbose_name = "Оценка выплаты ОСАГО-Авто"
        verbose_name_plural = "Оценки выплат ОСАГО-Авто"

    def __str__(self):
        return f"Оценка повреждений: {self.damage_character[:50]}... - {self.percentage_of_insurance_amount}%"


# Оценка выплаты ОСАГО-Жизнь
class OsagoLifePayoutAssessment(models.Model):
    damage_character = models.TextField(verbose_name="Характер повреждения")
    percentage_of_insurance_amount = models.FloatField(verbose_name="Процент от страховой суммы")
    theme = models.ForeignKey(DamageThemeOsagoLife, null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name="Тематика повреждения")

    class Meta:
        verbose_name = "Оценка выплаты ОСАГО-Жизнь"
        verbose_name_plural = "Оценки выплат ОСАГО-Жизнь"

    def __str__(self):
        return (f"Оценка страховых случаев жизни: {self.damage_character[:50]}... -"
                f" {self.percentage_of_insurance_amount}%")


# Обращение ОСАГО
class OsagoClaim(models.Model):
    osago_contract = models.ForeignKey(OsagoContract, on_delete=models.CASCADE, verbose_name="Договор ОСАГО")
    claim_date = models.DateTimeField(default=timezone.now, verbose_name="Дата обращения")
    description = models.TextField(verbose_name="Описание случая")
    payout_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2,
                                        verbose_name="Сумма выплаты")
    availability_id = models.ForeignKey(AppraiserSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name="Расписание Оценщика")
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Обращение ОСАГО"
        verbose_name_plural = "Обращения ОСАГО"

    def __str__(self):
        return (f"Обращение ОСАГО #{self.id} от {self.claim_date.strftime('%Y-%m-%d')} -"
                f" Сумма выплаты: {self.payout_amount}")


# Связь Обращение - Оценка ОСАГО-Авто
class OsagoClaimAutoAssessment(models.Model):
    osago_claim = models.ForeignKey(OsagoClaim, on_delete=models.CASCADE, verbose_name="Обращение ОСАГО")
    osago_auto_assessment = models.ForeignKey(OsagoAutoPayoutAssessment, on_delete=models.CASCADE,
                                              verbose_name="Оценка ОСАГО-Авто")

    class Meta:
        verbose_name = "Обращение - Оценка ОСАГО-Авто"
        verbose_name_plural = "Обращения - Оценки ОСАГО-Авто"

    def __str__(self):
        return f"Обращение #{self.osago_claim.id} - Оценка авто #{self.osago_auto_assessment.id}"


# Связь Обращение - Оценка ОСАГО-Жизнь
class OsagoClaimLifeAssessment(models.Model):
    osago_claim = models.ForeignKey(OsagoClaim, on_delete=models.CASCADE, verbose_name="Обращение ОСАГО")
    osago_life_assessment = models.ForeignKey(OsagoLifePayoutAssessment, on_delete=models.CASCADE,
                                              verbose_name="Оценка ОСАГО-Жизнь")

    class Meta:
        verbose_name = "Обращение - Оценка ОСАГО-Жизнь"
        verbose_name_plural = "Обращения - Оценки ОСАГО-Жизнь"

    def __str__(self):
        return f"Обращение #{self.osago_claim.id} - Оценка жизни #{self.osago_life_assessment.id}"
