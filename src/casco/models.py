from django.db import models
from django.utils import timezone

from src.authorization.models import CustomUser
from src.users.models import AgentSchedule, AppraiserSchedule


# Марка автомобиля
class Brand(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название марки")

    class Meta:
        verbose_name = "Марка"
        verbose_name_plural = "Марки"

    def __str__(self):
        return self.name


#  Модель автомобиля
class CarModel(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, verbose_name="Марка автомобиля")
    year = models.IntegerField(verbose_name="Год выпуска")
    horsepower = models.IntegerField(verbose_name="Лошадиные силы")
    model_name = models.CharField(max_length=255, verbose_name="Название модели")

    class Meta:
        verbose_name = "Модель автомобиля"
        verbose_name_plural = "Модели автомобилей"

    def __str__(self):
        return f"{self.brand.name} {self.model_name} ({self.year})"


#  Запись на прием Каско
class CascoRecord(models.Model):
    client_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")
    schedule = models.ForeignKey(AgentSchedule, null=True, blank=True, on_delete=models.CASCADE,
                                 verbose_name="Расписание агента")
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, verbose_name="Модель автомобиля")
    age = models.IntegerField(verbose_name="Возраст")
    experience = models.IntegerField(verbose_name="Стаж")
    COVERAGE_CHOICES = (
        ('full', 'Полное покрытие'),
        ('theft_destruction', 'Угон + гибель авто'),
        ('damage_destruction', 'Ущерб + гибель авто'),
    )
    coverage = models.CharField(max_length=20, choices=COVERAGE_CHOICES, verbose_name="Покрытие")
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
    REPAIR_TYPE_CHOICES = (
        ('dealer', 'Дилерский центр'),
        ('specialized_service', 'Специализированный сервис'),
        ('express_repair', 'Экспресс-ремонт'),
    )
    repair_type = models.CharField(max_length=255, choices=REPAIR_TYPE_CHOICES, verbose_name="Тип ремонта")
    mileage = models.IntegerField(verbose_name="Пробег")
    cost_guarantee = models.BooleanField(default=False, verbose_name="Гарантия стоимости")
    car_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость авто")

    class Meta:
        verbose_name = "Запись на прием Каско"
        verbose_name_plural = "Записи на прием Каско"

    def __str__(self):
        return f"Casco Record for {self.car_model.model_name} owned by {self.client_id.username}. Status: {self.status}"


# Договор Каско
class CascoContract(models.Model):
    agent_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Агент")
    casco_record = models.ForeignKey(CascoRecord, on_delete=models.CASCADE, verbose_name="Запись Каско")
    conclusion_date = models.DateTimeField(default=timezone.now, verbose_name="Дата заключения")
    start_date = models.DateField(verbose_name="Начало действия договора")
    end_date = models.DateField(verbose_name="Конец действия договора")

    class Meta:
        verbose_name = "Договор Каско"
        verbose_name_plural = "Договора Каско"

    def __str__(self):
        return f"Casco {self.id} from {self.start_date} to {self.end_date}"


class DamageTheme(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название тематики")

    class Meta:
        verbose_name = "Тема повреждения КАСКО"
        verbose_name_plural = "Темы повреждений КАСКО"

    def __str__(self):
        return self.name


# Оценка выплаты Каско
class CascoPayoutAssessment(models.Model):
    damage_character = models.TextField(verbose_name="Характер повреждения", unique=True)
    percentage_of_insurance_amount = models.FloatField(verbose_name="Процент от страховой суммы")
    theme = models.ForeignKey(DamageTheme, null=True, blank=True, on_delete=models.CASCADE,
                              verbose_name="Тематика повреждения")

    class Meta:
        verbose_name = "Оценка выплаты Каско"
        verbose_name_plural = "Оценки выплат Каско"

    def __str__(self):
        return f"Повреждение: {self.damage_character[:50]}... - {self.percentage_of_insurance_amount}%"


# Обращение КАСКО
class CascoClaim(models.Model):
    insurance_contract_id = models.ForeignKey(CascoContract, on_delete=models.CASCADE,
                                              verbose_name="Договор КАСКО")
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
        max_length=20, null=True, blank=True,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    class Meta:
        verbose_name = "Обращение КАСКО"
        verbose_name_plural = "Обращения КАСКО"

    def __str__(self):
        return f"Обращение #{self.id} - {self.claim_date.strftime('%Y-%m-%d')} - Сумма выплаты: {self.payout_amount}"


# Связь Обращение - Оценка КАСКО
class CascoClaimAssessment(models.Model):
    casco_claim = models.ForeignKey(CascoClaim, on_delete=models.CASCADE, verbose_name="Обращение КАСКО")
    payout_assessment = models.ForeignKey(CascoPayoutAssessment, on_delete=models.CASCADE, verbose_name="Оценка КАСКО")

    class Meta:
        verbose_name = "Связь Обращение - Оценка КАСКО"
        verbose_name_plural = "Связи Обращение - Оценка КАСКО"

    def __str__(self):
        return (f"Связь #{self.id} между обращением #{self.casco_claim.id} "
                f"и оценкой выплаты #{self.payout_assessment.id}")
