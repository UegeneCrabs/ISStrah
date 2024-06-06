from django.db import models
from django.utils import timezone

from src.authorization.models import CustomUser
from src.users.models import AgentSchedule, AppraiserSchedule


# Запись на прием по договору страхования квартиры
class HomeInsuranceRecord(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")
    schedule = models.ForeignKey(AgentSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name="Расписание агента")
    city = models.CharField(max_length=100, verbose_name="Город")
    street = models.CharField(max_length=100, verbose_name="Улица")
    house = models.CharField(max_length=10, verbose_name="Дом")
    apartment = models.CharField(max_length=10, verbose_name="Квартира")
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
    CHOICES = [
        (500000, '500 000 руб'),
        (1000000, '1 000 000 руб'),
        (1500000, '1 500 000 руб'),
        (2000000, '2 000 000 руб')
    ]
    interior_finish = models.PositiveIntegerField(choices=CHOICES, verbose_name="Внутренняя отделка")
    structural_elements = models.PositiveIntegerField(choices=CHOICES, verbose_name="Конструктивные элементы")
    civil_liability = models.PositiveIntegerField(choices=CHOICES, verbose_name="Гражданская ответственность")
    household_property = models.PositiveIntegerField(choices=CHOICES, verbose_name="Домашнее имущество")
    additional_protection = models.BooleanField(default=False, verbose_name="Дополнительная защита")
    war_risk = models.BooleanField(default=False, verbose_name="Риск военных действий")
    neighbor_repair_liability = models.BooleanField(default=False,
                                                    verbose_name="Ответственность перед соседями при ремонте")
    atmospheric_impact = models.BooleanField(default=False, verbose_name="Воздействие атмосферных осадков")

    class Meta:
        verbose_name = "Запись на прием по страхованию квартиры"
        verbose_name_plural = "Записи на прием по страхованию квартиры"

    def __str__(self):
        return f"Запись на прием по страхованию для {self.client} в {self.city}, ул. {self.street}, дом {self.house}. Статус: {self.status}"


# Договор страхования квартиры
class HomeInsuranceContract(models.Model):
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Агент")
    record = models.ForeignKey(HomeInsuranceRecord, on_delete=models.CASCADE, verbose_name="Запись")
    conclusion_date = models.DateTimeField(default=timezone.now, verbose_name="Дата заключения")
    start_date = models.DateField(verbose_name="Начало действия")
    end_date = models.DateField(verbose_name="Конец действия")

    class Meta:
        verbose_name = "Договор страхования квартиры"
        verbose_name_plural = "Договоры страхования квартир"

    def __str__(self):
        return f"Договор страхования квартиры #{self.id} от {self.start_date} до {self.end_date}"


class DamageThemeHome(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тематики")

    class Meta:
        verbose_name = "Тема повреждения Квартира"
        verbose_name_plural = "Темы повреждений Квартира"

    def __str__(self):
        return self.name


# Оценка выплаты квартира
class HomePayoutAssessment(models.Model):
    damage_character = models.TextField(verbose_name="Характер повреждения", unique=True)
    percentage_of_insurance_amount = models.FloatField(verbose_name="Процент от страховой суммы")
    theme = models.ForeignKey(DamageThemeHome, null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name="Тематика повреждения")

    class Meta:
        verbose_name = "Оценка выплаты по страхованию квартиры"
        verbose_name_plural = "Оценки выплат по страхованию квартиры"

    def __str__(self):
        return f"Оценка выплаты: {self.damage_character[:50]}... - {self.percentage_of_insurance_amount}%"


# Обращение по страховому случаю по страхованию квартиры
class HomeInsuranceClaim(models.Model):
    contract = models.ForeignKey(HomeInsuranceContract, on_delete=models.CASCADE,
                                 verbose_name="Договор страхования квартиры")
    appraiser = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE,
                                  verbose_name="Страховой оценщик")
    claim_date = models.DateTimeField(default=timezone.now, verbose_name="Дата обращения")
    description = models.TextField(verbose_name="Описание случая")
    payout_amount = models.DecimalField(max_digits=10, null=True, blank=True, decimal_places=2,
                                        verbose_name="Сумма выплаты")
    availability_id = models.ForeignKey(AppraiserSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                        verbose_name="Расписание Оценщика")
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
        verbose_name = "Обращение по страховому случаю квартиры"
        verbose_name_plural = "Обращения по страховым случаям квартир"

    def __str__(self):
        return f"Обращение #{self.id} от {self.claim_date.strftime('%Y-%m-%d')}"


# Обращение - Оценка квартиры
class HomeClaimAssessment(models.Model):
    claim = models.ForeignKey(HomeInsuranceClaim, on_delete=models.CASCADE,
                              verbose_name="Обращение по страхованию квартиры")
    assessment = models.ForeignKey(HomePayoutAssessment, on_delete=models.CASCADE, verbose_name="Оценка квартиры")

    class Meta:
        verbose_name = "Связь Обращения и Оценки по страхованию квартиры"
        verbose_name_plural = "Связи Обращений и Оценок по страхованию квартир"

    def __str__(self):
        return f"Связь обращения #{self.claim.id} с оценкой #{self.assessment.id}"
