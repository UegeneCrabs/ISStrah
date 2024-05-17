from django.shortcuts import render, redirect, get_object_or_404
from .forms import LifeInsuranceForm, LifeInsuranceSearchForm, LifeRecordForm, LifeInsuranceScheduleForm
from decimal import Decimal, InvalidOperation

from .models import LifeInsuranceRecord, LifeInsuranceContract, HealthClaim
from django.db.models import Q
import logging


def calculate_life_insurance_cost(duration, age, sport_coverage, sum_insurance, competition, additional_sports):
    base_rate = Decimal('500.0')  # Базовая ставка

    duration_rate = Decimal(duration)
    age_rate = Decimal(age)
    sport_coverage_rate = Decimal(sport_coverage)
    sum_insurance_rate = Decimal(sum_insurance)
    competition_rate = Decimal('1.2') if competition else Decimal('1.0')

    # Разделить additional_sports по запятой и посчитать количество видов спорта
    sports_list = additional_sports.split(',')
    sports_rate = Decimal('1.0') + Decimal('0.1') * len(sports_list)

    insurance_cost = base_rate * duration_rate * age_rate * sport_coverage_rate * sum_insurance_rate * competition_rate * sports_rate
    return insurance_cost.quantize(Decimal('0.01'))


def life_insurance_view(request):
    insurance_cost = None
    form = LifeInsuranceForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        competition = form.cleaned_data['competition_participation']
        duration = form.cleaned_data['insurance_duration']
        age = form.cleaned_data['age_coefficient']
        sport_coverage = form.cleaned_data['sport_coverage']
        sum_insurance = form.cleaned_data['sum_insurance']
        additional_sports = form.cleaned_data['additional_sports']
        insurance_cost = calculate_life_insurance_cost(duration, age, sport_coverage, sum_insurance, competition,
                                                       additional_sports)
    else:
        form = LifeInsuranceForm()

    return render(request, 'life/client/applications contract/calc_ins_health.html',
                  {'form': form, 'insurance_cost': insurance_cost})


def create_life_insurance_record(request):
    if request.method == 'POST':
        form = LifeInsuranceForm(request.POST)
        if form.is_valid():
            try:
                insurance_cost = request.POST.get('insurance_cost').replace(',', '.')
                insurance_cost_decimal = Decimal(insurance_cost)
            except (InvalidOperation, ValueError):
                return redirect('life:life_insurance_view')

            competition_participation = form.cleaned_data['competition_participation']
            additional_sports = form.cleaned_data['additional_sports']
            insurance_duration = form.cleaned_data['insurance_duration']
            age_coefficient = form.cleaned_data['age_coefficient']
            sport_coverage = form.cleaned_data['sport_coverage']
            sum_insurance = form.cleaned_data['sum_insurance']

            life_insurance_record = LifeInsuranceRecord(
                client=request.user,
                competition_participation=competition_participation,
                additional_sports=additional_sports,
                insurance_duration=insurance_duration,
                age_coefficient=age_coefficient,
                sport_coverage=sport_coverage,
                sum_insurance=sum_insurance,
                insurance_cost=insurance_cost_decimal
            )

            life_insurance_record.save()
            return redirect('life:user_life_insurance_requests')

    return redirect('life:life_insurance_view')


def user_life_insurance_requests(request):
    life_insurance_records = LifeInsuranceRecord.objects.filter(client=request.user)
    return render(request, 'life/client/applications contract/life_insurance_requests.html',
                  {'life_insurance_records': life_insurance_records})


def search_request_life_insurance(request):
    form = LifeInsuranceSearchForm(request.GET)
    life_insurance_records = LifeInsuranceRecord.objects.filter(client=request.user)

    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        insurance_duration = form.cleaned_data.get('insurance_duration')
        age_coefficient = form.cleaned_data.get('age_coefficient')
        sport_coverage = form.cleaned_data.get('sport_coverage')
        status = form.cleaned_data.get('status')
        sum_insurance = form.cleaned_data.get('sum_insurance')

        if search_query:
            life_insurance_records = life_insurance_records.filter(
                Q(additional_sports__icontains=search_query) |
                Q(insurance_duration__icontains=search_query) |
                Q(age_coefficient__icontains=search_query) |
                Q(sport_coverage__icontains=search_query) |
                Q(sum_insurance__icontains=search_query) |
                Q(insurance_cost__icontains=search_query)
            )

        if insurance_duration:
            life_insurance_records = life_insurance_records.filter(insurance_duration=insurance_duration)

        if age_coefficient:
            life_insurance_records = life_insurance_records.filter(age_coefficient=age_coefficient)

        if sport_coverage:
            life_insurance_records = life_insurance_records.filter(sport_coverage=sport_coverage)

        if status:
            life_insurance_records = life_insurance_records.filter(status=status)

        if sum_insurance:
            life_insurance_records = life_insurance_records.filter(sum_insurance=sum_insurance)

    return render(request, 'life/client/applications contract/life_insurance_requests.html',
                  {'form': form, 'life_insurance_records': life_insurance_records})


def client_life_insurance_contracts(request):
    contracts = LifeInsuranceContract.objects.filter(record__client=request.user)
    return render(request, 'life/client/contract/client_health_contracts.html', {'contracts': contracts})


def client_life_claims(request):
    claims = HealthClaim.objects.filter(insurance_contract__record__client=request.user)
    return render(request, 'life/client/applications insurance/client_life_claims.html', {'claims': claims})


logger = logging.getLogger(__name__)


def edit_life_record(request, record_id):
    try:
        record = get_object_or_404(LifeInsuranceRecord, id=record_id)
        if request.method == 'POST':
            form = LifeRecordForm(request.POST, instance=record)
            if form.is_valid():
                record = form.save(commit=False)  # Пока не сохраняем в базу
                # Обновляем стоимость страхования из скрытого поля
                record.insurance_cost = Decimal(request.POST.get('insurance_cost'))
                record.save()  # Сохраняем изменения
                return redirect('life:user_life_insurance_requests')  # Замените на нужную вам страницу
        else:
            form = LifeRecordForm(instance=record)
        return render(request, 'life/client/applications contract/edit_life_record.html',
                      {'form': form, 'record': record})
    except Exception as e:
        logger.error(f"Error in edit_casco_record view: {e}")
        return render(request, 'life/client/applications contract/edit_life_record.html',
                      {'form': None, 'error': str(e), 'record': record})


def delete_life_record(request, record_id):
    record = get_object_or_404(LifeInsuranceRecord, id=record_id)
    if request.method == 'POST':
        record.delete()
        return redirect('life:user_life_insurance_requests')
    return redirect('edit_casco_record', record_id=record_id)


def schedule_life_insurance_appointment(request, record_id):
    record = LifeInsuranceRecord.objects.get(id=record_id)
    if request.method == 'POST':
        form = LifeInsuranceScheduleForm(request.POST, instance=record)
        if form.is_valid():
            availability = form.cleaned_data['availability']
            availability.available = False
            availability.save()

            form.save()
            return redirect('life:user_life_insurance_requests')  # Перенаправление после успешной обработки
    else:
        form = LifeInsuranceScheduleForm(instance=record)

    return render(request, 'life/client/applications contract/schedule_life_insurance_appointment.html', {'form': form, 'record': record})
