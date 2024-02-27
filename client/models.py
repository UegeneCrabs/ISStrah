from django.db import models

from main.models import CustomUser


# ---------------------------------------------------OTHER------------------------------------------------------------

class Availability(models.Model):
    date = models.DateField()
    time = models.TimeField()
    available = models.BooleanField()

    def __str__(self):
        return f"{self.date} - {self.time}: {'Free' if self.available else 'Booked'}"


# ---------------------------------------------------HEALTH------------------------------------------------------------
class PaymentTableHealth(models.Model):
    nature_damage = models.CharField(verbose_name='Характер повреждения', max_length=255)
    percent = models.IntegerField(verbose_name='Процент от страх. суммы')

    def __str__(self):
        return f"{self.nature_damage} - {self.percent}%"


class AppointmentsHealth(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='appointments_health')
    available = models.ForeignKey(Availability, on_delete=models.CASCADE, verbose_name='Время')
    participation_in_competition = models.BooleanField(verbose_name='Участие в соревнованиях', null=True, default=False)
    additional_sports = models.CharField(verbose_name='Дополнительные виды спорта', null=True, max_length=100,
                                         default=False)

    DURATION_CHOICES = [
        (1, '1 год'),
        (1.2, '6 месяцев'),
        (1.3, '3 месяца'),
        (1.5, '1 месяц'),
    ]
    duration = models.FloatField(verbose_name='Длительность страхования', choices=DURATION_CHOICES, max_length=100)

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

    insurance_cost = models.FloatField(verbose_name='Стоимость страховки')
    is_active = models.BooleanField(verbose_name='Проработана', default=False, null=True)

    def __str__(self):
        return (f"{self.client.name} {self.client.surname} - {self.age_coefficient} лет,"
                f" срок страхования: {self.duration}, ({self.sum_insurance} СС). "
                f"Insurance cost - {self.insurance_cost}. Участие в соревнованиях={self.participation_in_competition}. "
                f"Проработана={self.is_active}")


class ContractHealth(models.Model):
    appointment = models.ForeignKey(AppointmentsHealth, on_delete=models.CASCADE, verbose_name='Запись')
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Страховой агент',
                              related_name='contract_health_agent')
    date_signing = models.DateField()

    def __str__(self):
        return (
            f"{self.appointment.client.name} {self.appointment.client.surname} - {self.appointment.age_coefficient} лет,"
            f" срок страхования: {self.appointment.duration}, ({self.appointment.sum_insurance} СС). "
            f"Insurance cost - {self.appointment.insurance_cost}."
            f" Участие в соревнованиях={self.appointment.participation_in_competition}. "
            f"Проработана={self.appointment.is_active}")


class AppealHealth(models.Model):
    contract = models.ForeignKey(ContractHealth, on_delete=models.CASCADE, verbose_name='Договор', null=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appeal_agent_health', verbose_name='Договор', null=True)
    payment_amount = models.FloatField(verbose_name='Сумма выплаты', null=True)
    nature_damage = models.CharField(verbose_name='Опись повреждения', max_length=255, null=True)
    payment_table = models.ForeignKey(PaymentTableHealth, on_delete=models.CASCADE, verbose_name='Таблица выплат', null=True)


# -----------------------------------------------------CAR------------------------------------------------------------

class PaymentTableCar(models.Model):
    nature_damage_car = models.CharField(verbose_name='Характер повреждения', max_length=255)
    percent_car = models.IntegerField(verbose_name='Процент от страх. суммы')

    def __str__(self):
        return f"{self.nature_damage_car} - {self.percent_car}%"


class AppointmentsCar(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Клиент',
                               related_name='appointments_car')
    available = models.ForeignKey(Availability, on_delete=models.CASCADE, verbose_name='Время')
    brand = models.CharField(verbose_name='Марка авто', max_length=100)
    model = models.CharField(verbose_name='Модель авто', max_length=100)
    car_year = models.IntegerField(verbose_name='Год выпуска')
    horse_power = models.IntegerField(verbose_name='Лошадиные силы')
    DRIVER_CHOICES = [
        ('one_person', 'Один человек'),
        ('unlimited', 'Неограниченное количество'),
    ]
    driver_option = models.CharField(verbose_name='Количество лиц допущенных к управлению', choices=DRIVER_CHOICES,
                                     max_length=100)
    age = models.IntegerField(verbose_name='Возраст')
    experience = models.IntegerField(verbose_name='Стаж')
    insurance_cost = models.FloatField(verbose_name='Стоимость страховки')
    is_active = models.BooleanField(verbose_name='Проработана', default=False, null=True)

    def __str__(self):
        return (f"{self.client.name} - {self.brand} {self.model}, {self.car_year} year, ({self.horse_power}HS)."
                f" Insurance cost - {self.insurance_cost}. Проработана: {self.is_active}")


class ContractCar(models.Model):
    appointment = models.ForeignKey(AppointmentsCar, on_delete=models.CASCADE, verbose_name='Запись')
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Страховой агент',
                              related_name='contract_car_agent')  # Изменено имя обратной связи
    date_signing = models.DateField()

    def __str__(self):
        return (
            f"{self.appointment.client.name} {self.appointment.client.surname} - {self.appointment.brand} {self.appointment.model}, {self.appointment.car_year} year, ({self.appointment.horse_power}HS)."
            f" Insurance cost - {self.appointment.insurance_cost}")


class AppealCar(models.Model):
    contract_car = models.ForeignKey(ContractCar, on_delete=models.CASCADE, verbose_name='Договор', null=True)
    agent = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='appeal_agent_car', verbose_name='Договор', null=True)
    payment_amount = models.FloatField(verbose_name='Сумма выплаты', null=True)
    nature_damage = models.CharField(verbose_name='Опись повреждения', max_length=255, null=True)
    payment_table = models.ForeignKey(PaymentTableCar, on_delete=models.CASCADE, verbose_name='Таблица выплат', null=True)
