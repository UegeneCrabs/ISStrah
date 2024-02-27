from django.contrib.auth.decorators import login_required

from client.forms import (HealthInsuranceCalculatorForm, InsuranceCalculatorForm, DateSelectionForm,
                          AppointmentsCarForm, AppointmentsHealthForm)
from django.shortcuts import redirect

from django.db import IntegrityError
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import (AppointmentsCar, Availability, AppointmentsHealth, ContractHealth, PaymentTableHealth, ContractCar,
                     PaymentTableCar)
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib import messages


# ---------------------------------------------------OTHER------------------------------------------------------------
@login_required
def select_date(request):
    availability_obj = None
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            selected_date = form.cleaned_data['available_dates']
            availability_obj = Availability.objects.get(date=selected_date)
    else:
        form = DateSelectionForm()
    return render(request, 'client/date_selection.html', {'form': form,
                                                          'availability_obj': availability_obj})


@receiver(post_delete, sender=AppointmentsCar)
def update_availability(sender, instance, **kwargs):
    try:
        availability = Availability.objects.get(id=instance.available.id)
        availability.available = True
        availability.save()
    except Availability.DoesNotExist:
        pass


@receiver(post_delete, sender=AppointmentsHealth)
def update_availability(sender, instance, **kwargs):
    try:
        availability = Availability.objects.get(id=instance.available.id)
        availability.available = True
        availability.save()
    except Availability.DoesNotExist:
        pass


# ---------------------------------------------------HEALTH-----------------------------------------------------------
@login_required
def health_contracts(request):
    contracts = ContractHealth.objects.filter(appointment__client=request.user)
    payment_table = PaymentTableHealth.objects.all()
    return render(request, 'client/health_contracts.html', {'contracts': contracts,
                                                            'payment_table': payment_table})


@login_required
def calc_ins_health(request):
    context = {}
    insurance_cost = None
    if request.method == 'POST':
        health_insurance_form = HealthInsuranceCalculatorForm(request.POST)
        if health_insurance_form.is_valid():
            duration = health_insurance_form.cleaned_data['duration']
            age_coefficient = health_insurance_form.cleaned_data['age_coefficient']
            sport_coverage = health_insurance_form.cleaned_data['sport_coverage']
            sum_insurance = health_insurance_form.cleaned_data['sum_insurance']
            additional_sports = health_insurance_form.cleaned_data['additional_sports']
            participation_in_competition = health_insurance_form.cleaned_data['participation_in_competition']

            insurance_cost = calculate_insurance_health_cost(duration, age_coefficient,
                                                             sport_coverage, additional_sports,
                                                             participation_in_competition, sum_insurance)
            context = {
                'duration': duration,
                'age_coefficient': age_coefficient,
                'sport_coverage': sport_coverage,
                'sum_insurance': sum_insurance,
                'additional_sports': additional_sports,
                'participation_in_competition': participation_in_competition,
                'insurance_cost': insurance_cost,
            }
    else:
        health_insurance_form = HealthInsuranceCalculatorForm()

    return render(request, 'client/calc_ins_health.html', {
        'title': 'calc_ins_health',
        'health_insurance_form': health_insurance_form,
        'insurance_cost': insurance_cost,
        'context': context,
    })


def calculate_insurance_health_cost(duration, age_coefficient, sport_coverage, additional_sports,
                                    participation_in_competition, sum_insurance):
    tb = 500
    additional_sc = 1 + (0.1 * len(additional_sports.split(','))) if additional_sports else 1

    participation_in_cc = 1.2 if participation_in_competition else 1
    duration = float(duration)
    age_coefficient = float(age_coefficient)
    sport_coverage = float(sport_coverage)
    sum_insurance = float(sum_insurance)
    insurance_cost = (tb * duration * age_coefficient * sport_coverage * additional_sc
                      * participation_in_cc * sum_insurance)
    return round(insurance_cost, 2)


@login_required
def add_appointment_health(request):
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():

            available = form.cleaned_data['available_dates']
            participation_in_competition = request.GET['participation_in_competition']
            additional_sports = request.GET['additional_sports']
            duration = request.GET['duration']
            age_coefficient = request.GET['age_coefficient']
            sport_coverage = request.GET['sport_coverage']
            sum_insurance = request.GET['sum_insurance']
            insurance_cost = float(request.GET['insurance_cost'].replace(',', '.'))

            try:
                appointment_health = AppointmentsHealth.objects.create(
                    client=request.user,
                    available=available,
                    participation_in_competition=participation_in_competition,
                    additional_sports=additional_sports,
                    duration=duration,
                    age_coefficient=age_coefficient,
                    sport_coverage=sport_coverage,
                    sum_insurance=sum_insurance,
                    insurance_cost=insurance_cost
                )
            except IntegrityError:
                # Ошибка при сохранении записи
                appointment_health = None

            if appointment_health:
                # Запись успешно сохранена
                available.available = False
                available.save()
                return redirect("personalaccountclient")
            else:
                pass
    else:
        form = DateSelectionForm()

    return render(request, 'client/add_appointment_health.html', {'form': form})


def edit_appointment_health(request, appointment_health_id):
    appointment_health = get_object_or_404(AppointmentsHealth, id=appointment_health_id)

    if request.method == 'POST':
        form = AppointmentsHealthForm(request.POST, instance=appointment_health)
        if form.is_valid():
            participation_in_competition = form.cleaned_data['participation_in_competition']
            additional_sports = form.cleaned_data['additional_sports']
            duration = form.cleaned_data['duration']
            age_coefficient = form.cleaned_data['age_coefficient']
            sport_coverage = form.cleaned_data['sport_coverage']
            sum_insurance = form.cleaned_data['sum_insurance']
            insurance_cost = calculate_insurance_health_cost(duration, age_coefficient,
                                                             sport_coverage, additional_sports,
                                                             participation_in_competition, sum_insurance)
            appointment_health.insurance_cost = insurance_cost
            form.save()
            return redirect('client_requests_health')
    else:
        form = AppointmentsHealthForm(instance=appointment_health)

    return render(request, 'client/edit_appointment_health.html',
                  {'form': form, 'appointment_health': appointment_health})


def delete_appointment_health(request, appointment_health_id):
    appointment_health = get_object_or_404(AppointmentsHealth, id=appointment_health_id)

    if request.method == 'POST':
        appointment_health.delete()
        return redirect('client_requests_health')  # Перенаправление на страницу списка записей
    return redirect('edit_appointment_health', appointment_health_id=appointment_health_id)


# ---------------------------------------------------CLIENT-----------------------------------------------------------

@login_required
def personal_account_client(request):
    user = request.user
    return render(request, 'client/personalaccountclient.html', {
        'title': 'personalaccountclient',
        'user': user,
    })


@login_required
def client_requests_car(request):
    appointments_car = AppointmentsCar.objects.filter(client=request.user)

    return render(request, 'client/client_requests_car.html', {
        'title': 'client_requests_car',
        'appointments_car': appointments_car,
    })


@login_required
def client_requests_health(request):
    appointments_health = AppointmentsHealth.objects.filter(client=request.user)

    return render(request, 'client/client_requests_health.html', {
        'title': 'client_requests_health',
        'appointments_health': appointments_health,
    })


@login_required
def profile(request):
    user = request.user
    appointments_health = AppointmentsHealth.objects.filter(client=user)
    contracts_health = []

    for appointment_health in appointments_health:
        if ContractHealth.objects.filter(appointment=appointment_health).exists():
            contract_health = get_object_or_404(ContractHealth, appointment=appointment_health)
            contracts_health.append(contract_health)

    appointments_car = AppointmentsCar.objects.filter(client=user)
    contracts_car = []

    for appointment_car in appointments_car:
        if ContractCar.objects.filter(appointment=appointment_car).exists():
            contract_car = get_object_or_404(ContractCar, appointment=appointment_car)
            contracts_car.append(contract_car)

    print("Appointments Car:")
    for appointment_car in appointments_car:
        print(appointment_car)

    print("\nContracts Car:")
    for contract_car in contracts_car:
        print(contract_car)

    print("Appointments Health:")
    for appointment_health in appointments_health:
        print(appointment_health)

    print("\nContracts Health:")
    for contract_health in contracts_health:
        print(contract_health)
    return render(request, 'client/profile.html', {'user': user,
                                                   'appointments_health': appointments_health,
                                                   'appointments_car': appointments_car,
                                                   'contracts_health': contracts_health,
                                                   'contracts_car': contracts_car})


# ---------------------------------------------------AGENT------------------------------------------------------------

@login_required
def agent_profile(request):
    user = request.user
    return render(request, 'client/agent_profile.html', {'user': user})


@login_required
def personal_account_employee(request):
    user = request.user
    return render(request, 'client/personalaccountemployee.html',
                  {"title": "personalaccountemployee", "user": user})


@login_required
def agent_requests_car(request):
    appointments_car = AppointmentsCar.objects.filter(is_active=False)

    return render(request, 'client/agent_requests_car.html', {
        'title': 'agent_requests_car',
        'appointments_car': appointments_car,
    })


@login_required
def agent_requests_health(request):
    appointments_health = AppointmentsHealth.objects.filter(is_active=False)

    return render(request, 'client/agent_requests_health.html', {
        'title': 'agent_requests_health',
        'appointments_health': appointments_health,
    })


@login_required
def agent_requests_car_contract(request):
    contracts = ContractCar.objects.all()
    payment_table = PaymentTableCar.objects.all()
    return render(request, 'client/agent_requests_car_contract.html', {
        'title': 'agent_requests_car_contract',
        'contracts': contracts,
        'payment_table': payment_table,
    })


@login_required
def agent_requests_health_contract(request):
    contracts = ContractHealth.objects.all()
    payment_table = PaymentTableHealth.objects.all()
    return render(request, 'client/agent_requests_health_contract.html', {
        'title': 'agent_requests_health_contract',
        'contracts': contracts,
        'payment_table': payment_table,
    })


@login_required
def create_contract_health(request, appointment_id):
    if request.method == 'GET':
        appointment = AppointmentsHealth.objects.get(pk=appointment_id)
        contract_health = ContractHealth.objects.create(appointment=appointment,
                                                        agent=request.user,
                                                        date_signing=timezone.now())
        contract_health.save()
        if contract_health.pk:
            appointment.is_active = True
            appointment.save()
            return redirect('agent_requests_health_contract')
        else:
            messages.error(request, 'Ошибка при создании договора')
            return redirect('agent_requests_health')
    else:
        return render(request, 'client/agent_requests_health.html', {'appointment_id': appointment_id})


@login_required
def create_contract_car(request, appointment_id):
    if request.method == 'GET':
        appointment = AppointmentsCar.objects.get(pk=appointment_id)
        contract_car = ContractCar.objects.create(appointment=appointment,
                                                  agent=request.user,
                                                  date_signing=timezone.now())
        contract_car.save()
        if contract_car.pk:
            appointment.is_active = True
            appointment.save()
            return redirect('agent_requests_car_contract')
        else:
            messages.error(request, 'Ошибка при создании договора')
            return redirect('agent_requests_car')
    else:
        return render(request, 'client/agent_requests_car.html', {'appointment_id': appointment_id})


# -----------------------------------------------------CAR------------------------------------------------------------
@login_required
def car_contracts(request):
    appointments_car = AppointmentsCar.objects.filter(client=request.user)
    contracts = ContractCar.objects.filter(appointment__in=appointments_car)
    payment_table = PaymentTableCar.objects.all()
    return render(request, 'client/car_contracts.html', {'contracts': contracts,
                                                         'payment_table': payment_table})


@login_required
def appeal_car(request):
    return render(request, 'client/appeal_car.html', {'title': 'appeal_car'})


def calculate_insurance_cost(horse_power, driver_option, age, experience):
    tariff = 5000  # Базовый тариф
    kt = 1.8  # Коэффициент территории
    if driver_option == 'one_person':
        do = 1
    else:
        do = 1.8
    # Расчет коэффициента мощности авто (КМ)
    if horse_power < 50:
        km = 0.6
    elif 50 <= horse_power < 70:
        km = 1
    elif 70 <= horse_power < 100:
        km = 1.1
    elif 100 <= horse_power < 120:
        km = 1.2
    elif 120 <= horse_power < 150:
        km = 1.4
    else:
        km = 1.6

    # Расчет коэффициента возраста и стажа (КВС)
    if age <= 22 and experience <= 3:
        kvs = 1.8
    elif age > 22 and experience <= 3:
        kvs = 1.7
    elif age <= 22 and experience > 3:
        kvs = 1.6
    else:
        kvs = 1

    insurance_cost = tariff * kt * km * kvs * do
    return insurance_cost


@login_required
def calc_ins_auto(request):
    insurance_cost = None
    context = {}
    if request.method == 'POST':
        car_insurance_form = InsuranceCalculatorForm(request.POST)
        if car_insurance_form.is_valid():
            brand = car_insurance_form.cleaned_data['brand']
            model = car_insurance_form.cleaned_data['model']
            car_year = car_insurance_form.cleaned_data['car_year']
            horse_power = car_insurance_form.cleaned_data['horse_power']
            driver_option = car_insurance_form.cleaned_data['driver_option']
            age = car_insurance_form.cleaned_data['age']
            experience = car_insurance_form.cleaned_data['experience']

            insurance_cost = calculate_insurance_cost(horse_power, driver_option, age, experience)
            context = {
                'brand': brand,
                'model': model,
                'car_year': car_year,
                'horse_power': horse_power,
                'driver_option': driver_option,
                'age': age,
                'experience': experience,
                'insurance_cost': insurance_cost,
            }

    else:
        car_insurance_form = InsuranceCalculatorForm()

    return render(request, 'client/calc_ins_auto.html', {
        'title': 'calc_ins_auto',
        'car_insurance_form': car_insurance_form,
        'insurance_cost': insurance_cost,
        'context': context,
    })


@login_required
def add_appointment(request):
    if request.method == 'POST':
        form = DateSelectionForm(request.POST)
        if form.is_valid():
            available = form.cleaned_data['available_dates']
            brand = request.GET['brand']
            model = request.GET['model']
            car_year = request.GET['car_year']
            horse_power = request.GET['horse_power']
            driver_option = request.GET['driver_option']
            age = request.GET['age']
            experience = request.GET['experience']
            insurance_cost = float(request.GET['insurance_cost'].replace(',', '.'))

            try:
                appointment = AppointmentsCar.objects.create(
                    client=request.user,
                    available=available,
                    brand=brand,
                    model=model,
                    car_year=car_year,
                    horse_power=horse_power,
                    driver_option=driver_option,
                    age=age,
                    experience=experience,
                    insurance_cost=insurance_cost
                )
            except IntegrityError:
                appointment = None

            if appointment:
                available.available = False
                available.save()
                return redirect("personalaccountclient")
            else:
                pass
    else:
        form = DateSelectionForm()

    return render(request, 'client/add_appointment.html', {'form': form})


def edit_appointment_car(request, appointment_id):
    appointment = get_object_or_404(AppointmentsCar, id=appointment_id)
    if request.method == 'POST':
        form = AppointmentsCarForm(request.POST, instance=appointment)
        if form.is_valid():
            horse_power = form.cleaned_data['horse_power']
            driver_option = form.cleaned_data['driver_option']
            age = form.cleaned_data['age']
            experience = form.cleaned_data['experience']

            insurance_cost = calculate_insurance_cost(horse_power, driver_option, age, experience)
            appointment.insurance_cost = insurance_cost
            form.save()
            return redirect('client_requests_car')
    else:
        form = AppointmentsCarForm(instance=appointment)
    return render(request, 'client/edit_appointment_car.html', {'form': form,
                                                                'appointment': appointment})


def delete_appointment_car(request, appointment_id):
    appointment = get_object_or_404(AppointmentsCar, id=appointment_id)
    if request.method == 'POST':
        appointment.delete()
        return redirect('client_requests_car')
    return redirect('edit_appointment_car', appointment_id=appointment_id)
