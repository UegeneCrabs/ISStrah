from django.db import models
from django.utils import timezone

from src.authorization.models import CustomUser
from src.users.models import AgentSchedule, AppraiserSchedule


# Запись на прием жизнь
class LifeInsuranceRecord(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")
    availability = models.ForeignKey(AgentSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                     verbose_name="Доступность")
    competition_participation = models.BooleanField(verbose_name="Участие в соревнованиях", null=True, blank=True)
    additional_sports = models.TextField(verbose_name="Дополнительные виды спорта")

    DURATION_CHOICES = [
        (1, '1 год'),
        (1.2, '6 месяцев'),
        (1.3, '3 месяца'),
        (1.5, '1 месяц'),
    ]
    insurance_duration = models.FloatField(verbose_name='Длительность страхования', choices=DURATION_CHOICES,
                                           max_length=100)
    AGE_CHOICES = [
        (1, 'От 3 до 17 лет'),
        (1.5, 'От 18 до 35 лет'),
        (1.8, 'От 36 до 65 лет'),
    ]
    age_coefficient = models.FloatField(verbose_name='Возрастной коэффициент', choices=AGE_CHOICES, max_length=100)

    SPORT_COVERAGE_CHOICES = [
        (1.2, 'Обычный'),
        (1.4, 'Расширенный'),
    ]
    sport_coverage = models.FloatField(verbose_name='Категория спортивного покрытия', choices=SPORT_COVERAGE_CHOICES,
                                       max_length=100)

    SUM_INSURANCE_CHOICES = [
        (1.1, '100.000'),
        (1.3, '250.000'),
        (1.5, '500.000'),
    ]
    sum_insurance = models.FloatField(verbose_name='Сумма страхования', choices=SUM_INSURANCE_CHOICES, max_length=100)
    insurance_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость страховки")
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
    ]

    status = models.CharField(
        max_length=20, null=True, blank=True,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Запись на прием по страхованию жизни"
        verbose_name_plural = "Записи на прием по страхованию жизни"

    def __str__(self):
        return (f"{self.client.name} {self.client.surname},"
                f" срок страхования: {self.insurance_duration}, ({self.sum_insurance} СС)."
                f"Insurance cost - {self.insurance_cost}. Участие в соревнованиях={self.competition_participation}."
                f"Статус={self.status}")


# Договор страхования жизни
class LifeInsuranceContract(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Агент")
    record = models.ForeignKey(LifeInsuranceRecord, on_delete=models.CASCADE, verbose_name="Запись")
    conclusion_date = models.DateTimeField(default=timezone.now, verbose_name="Дата заключения")
    start_date = models.DateField(verbose_name="Начало действия")
    end_date = models.DateField(verbose_name="Конец действия")

    class Meta:
        verbose_name = "Договор страхования жизни"
        verbose_name_plural = "Договоры страхования жизни"

    def __str__(self):
        return (
            f"{self.record.client.name} {self.record.client.surname} - {self.record.age_coefficient} лет,"
            f" Срок страхования: {self.record.insurance_duration}, ({self.record.sum_insurance} СС). "
            f"Insurance cost - {self.record.insurance_cost}."
            f" Участие в соревнованиях={self.record.competition_participation}. "
            f"Проработана={self.record.status}")


# Обращение здоровье
class HealthClaim(models.Model):
    insurance_contract = models.ForeignKey(LifeInsuranceContract, on_delete=models.CASCADE,
                                           verbose_name="Договор страхования здоровья")
    claim_date = models.DateTimeField(default=timezone.now, verbose_name="Дата обращения")
    description = models.TextField(verbose_name="Описание случая")
    payout_amount = models.DecimalField(null=True, blank=True, max_digits=10, decimal_places=2,
                                        verbose_name="Сумма выплаты")
    schedule = models.ForeignKey(AppraiserSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name="Расписание оценщика")
    STATUS_CHOICES = [
        ('pending', 'Ожидает'),
        ('in_progress', 'В работе'),
        ('completed', 'Завершена'),
    ]

    status = models.CharField(
        max_length=20, null=True, blank=True,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Обращение по страхованию здоровья"
        verbose_name_plural = "Обращения по страхованию здоровья"

    def __str__(self):
        return f"Обращение по страхованию здоровья #{self.id} от {self.claim_date.strftime('%Y-%m-%d')}"


# Оценка выплаты Жизнь
class LifePayoutAssessment(models.Model):
    damage_character = models.TextField(verbose_name="Характер повреждения", unique=True)
    percentage_of_insurance_amount = models.FloatField(verbose_name="Процент от страховой суммы")

    class Meta:
        verbose_name = "Оценка выплаты по страхованию жизни"
        verbose_name_plural = "Оценки выплат по страхованию жизни"

    def __str__(self):
        return f"Оценка выплаты: {self.damage_character[:50]}... - {self.percentage_of_insurance_amount}%"


# Обращение - Оценка Жизнь
class LifeClaimAssessment(models.Model):
    life_claim = models.ForeignKey(HealthClaim, on_delete=models.CASCADE, verbose_name="Обращение жизни")
    life_assessment = models.ForeignKey(LifePayoutAssessment, on_delete=models.CASCADE, verbose_name="Оценка жизни")

    class Meta:
        verbose_name = "Связь обращения и оценки по страхованию жизни"
        verbose_name_plural = "Связи обращений и оценок по страхованию жизни"

    def __str__(self):
        return f"Связь обращения #{self.life_claim.id} с оценкой #{self.life_assessment.id}"
